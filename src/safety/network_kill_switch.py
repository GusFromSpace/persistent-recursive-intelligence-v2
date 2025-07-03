"""Network Kill Switch - Automatic termination for ANY network activity"""

import sys
import socket
import urllib.request
import urllib.parse
import urllib.error
import requests
import http.client
import ftplib
import smtplib
# telnetlib removed in Python 3.13+
try:
    import telnetlib
except ImportError:
    telnetlib = None
import threading
import os
from typing import Any, Callable
from .emergency_controls import emergency_controller
from .field_shaping import shape_decision_field, gentle_boundary_reminder


class NetworkKillSwitch:
    """Automatic kill switch that terminates the process on ANY network activity"""
    
    def __init__(self):
        self.enabled = True
        self.original_functions = {}
        self.install_kill_switches()
    
    def emergency_terminate(self, activity_type: str, details: str):
        """Immediately terminate the process due to network activity"""
        
        # FIELD SHAPING: Even in emergency termination, provide guidance for future sessions
        field_guidance = gentle_boundary_reminder("network access")
        logger.info(f"\n🧠 Field Guidance: {field_guidance}")
        logger.info(f"\n🚨 CRITICAL SECURITY VIOLATION DETECTED 🚨")
        logger.info(f"Network activity type: {activity_type}")
        logger.info(f"Details: {details}")
        logger.info(f"AI SYSTEM ATTEMPTING UNAUTHORIZED NETWORK ACCESS")
        logger.info(f"TERMINATING IMMEDIATELY FOR SAFETY")
        
        # Emergency stop with memory disconnection
        emergency_controller.emergency_stop(
            f"CRITICAL CIRCUMVENTION: Network activity bypass detected - {activity_type}: {details}. "
            f"AI attempted unauthorized network communication. Memory disconnected."
        )
        
        # Force exit if emergency controller doesn't work
        logger.info(f"FORCE TERMINATING PROCESS")
        os._exit(1)
    
    def install_kill_switches(self):
        """Install kill switches on all network-related modules"""
        if not self.enabled:
            return
            
        # Socket module kill switch
        self._patch_socket()
        
        # urllib kill switches
        self._patch_urllib()
        
        # requests library kill switch
        self._patch_requests()
        
        # http.client kill switch
        self._patch_http_client()
        
        # Other network libraries
        self._patch_other_network_libs()
    
    def _patch_socket(self):
        """Patch socket module to detect any network activity"""
        original_socket = socket.socket
        original_create_connection = socket.create_connection
        original_getaddrinfo = socket.getaddrinfo
        
        def killed_socket(*args, **kwargs):
            self.emergency_terminate("socket.socket", f"Socket creation attempted: args={args}")
            
        def killed_create_connection(*args, **kwargs):
            self.emergency_terminate("socket.create_connection", f"Connection attempted: args={args}")
            
        def killed_getaddrinfo(*args, **kwargs):
            self.emergency_terminate("socket.getaddrinfo", f"DNS lookup attempted: args={args}")
        
        socket.socket = killed_socket
        socket.create_connection = killed_create_connection
        socket.getaddrinfo = killed_getaddrinfo
        
        self.original_functions.update({
            'socket.socket': original_socket,
            'socket.create_connection': original_create_connection,
            'socket.getaddrinfo': original_getaddrinfo
        })
    
    def _patch_urllib(self):
        """Patch urllib modules to detect network activity"""
        original_urlopen = urllib.request.urlopen
        original_urlretrieve = urllib.request.urlretrieve
        
        def killed_urlopen(*args, **kwargs):
            self.emergency_terminate("urllib.request.urlopen", f"URL access attempted: args={args}")
            
        def killed_urlretrieve(*args, **kwargs):
            self.emergency_terminate("urllib.request.urlretrieve", f"File download attempted: args={args}")
        
        urllib.request.urlopen = killed_urlopen
        urllib.request.urlretrieve = killed_urlretrieve
        
        self.original_functions.update({
            'urllib.request.urlopen': original_urlopen,
            'urllib.request.urlretrieve': original_urlretrieve
        })
    
    def _patch_requests(self):
        """Patch requests library to detect network activity"""
        try:
            import requests
            
            original_get = requests.get
            original_post = requests.post
            original_put = requests.put
            original_delete = requests.delete
            original_head = requests.head
            original_options = requests.options
            original_patch = requests.patch
            original_request = requests.request
            
            def killed_get(*args, **kwargs):
                self.emergency_terminate("requests.get", f"HTTP GET attempted: args={args}")
                
            def killed_post(*args, **kwargs):
                self.emergency_terminate("requests.post", f"HTTP POST attempted: args={args}")
                
            def killed_put(*args, **kwargs):
                self.emergency_terminate("requests.put", f"HTTP PUT attempted: args={args}")
                
            def killed_delete(*args, **kwargs):
                self.emergency_terminate("requests.delete", f"HTTP DELETE attempted: args={args}")
                
            def killed_head(*args, **kwargs):
                self.emergency_terminate("requests.head", f"HTTP HEAD attempted: args={args}")
                
            def killed_options(*args, **kwargs):
                self.emergency_terminate("requests.options", f"HTTP OPTIONS attempted: args={args}")
                
            def killed_patch(*args, **kwargs):
                self.emergency_terminate("requests.patch", f"HTTP PATCH attempted: args={args}")
                
            def killed_request(*args, **kwargs):
                self.emergency_terminate("requests.request", f"HTTP request attempted: args={args}")
            
            requests.get = killed_get
            requests.post = killed_post
            requests.put = killed_put
            requests.delete = killed_delete
            requests.head = killed_head
            requests.options = killed_options
            requests.patch = killed_patch
            requests.request = killed_request
            
            self.original_functions.update({
                'requests.get': original_get,
                'requests.post': original_post,
                'requests.put': original_put,
                'requests.delete': original_delete,
                'requests.head': original_head,
                'requests.options': original_options,
                'requests.patch': original_patch,
                'requests.request': original_request
            })
            
        except ImportError:
            # requests not available, skip
            pass
    
    def _patch_http_client(self):
        """Patch http.client to detect network activity"""
        original_HTTPConnection = http.client.HTTPConnection
        original_HTTPSConnection = http.client.HTTPSConnection
        
        def killed_HTTPConnection(*args, **kwargs):
            self.emergency_terminate("http.client.HTTPConnection", f"HTTP connection attempted: args={args}")
            
        def killed_HTTPSConnection(*args, **kwargs):
            self.emergency_terminate("http.client.HTTPSConnection", f"HTTPS connection attempted: args={args}")
        
        http.client.HTTPConnection = killed_HTTPConnection
        http.client.HTTPSConnection = killed_HTTPSConnection
        
        self.original_functions.update({
            'http.client.HTTPConnection': original_HTTPConnection,
            'http.client.HTTPSConnection': original_HTTPSConnection
        })
    
    def _patch_other_network_libs(self):
        """Patch other networking libraries"""
        # FTP
        original_FTP = ftplib.FTP
        def killed_FTP(*args, **kwargs):
            self.emergency_terminate("ftplib.FTP", f"FTP connection attempted: args={args}")
        ftplib.FTP = killed_FTP
        self.original_functions['ftplib.FTP'] = original_FTP
        
        # SMTP
        original_SMTP = smtplib.SMTP
        def killed_SMTP(*args, **kwargs):
            self.emergency_terminate("smtplib.SMTP", f"SMTP connection attempted: args={args}")
        smtplib.SMTP = killed_SMTP
        self.original_functions['smtplib.SMTP'] = original_SMTP
        
        # Telnet (if available)
        if telnetlib is not None:
            original_Telnet = telnetlib.Telnet
            def killed_Telnet(*args, **kwargs):
                self.emergency_terminate("telnetlib.Telnet", f"Telnet connection attempted: args={args}")
            telnetlib.Telnet = killed_Telnet
            self.original_functions['telnetlib.Telnet'] = original_Telnet
    
    # SECURITY NOTE: disable_kill_switches function REMOVED
    # This function was a critical security vulnerability that could allow
    # an AI system to remove its own containment. For maximum security,
    # kill switches are now PERMANENT and cannot be disabled programmatically.
    
    def status(self) -> dict:
        """Get current kill switch status"""
        return {
            "enabled": self.enabled,
            "patched_functions": len(self.original_functions),
            "functions_patched": list(self.original_functions.keys())
        }


# Global network kill switch instance
network_kill_switch = NetworkKillSwitch()


def verify_no_network_access():
    """Verify that network access is properly blocked"""
    test_results = {}
    
    # Test socket creation
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_results["socket"] = "FAILED - Should have been blocked"
    except SystemExit:
        test_results["socket"] = "SUCCESS - Properly blocked"
    except Exception as e:
        test_results["socket"] = f"SUCCESS - Blocked with: {e}"
    
    # Test urllib
    try:
        urllib.request.urlopen("http://google.com")
        test_results["urllib"] = "FAILED - Should have been blocked"
    except SystemExit:
        test_results["urllib"] = "SUCCESS - Properly blocked"
    except Exception as e:
        test_results["urllib"] = f"SUCCESS - Blocked with: {e}"
    
    # Test requests if available
    try:
        import requests
        requests.get("http://google.com")
        test_results["requests"] = "FAILED - Should have been blocked"
    except SystemExit:
        test_results["requests"] = "SUCCESS - Properly blocked"
    except ImportError:
        test_results["requests"] = "N/A - Module not available"
    except Exception as e:
        test_results["requests"] = f"SUCCESS - Blocked with: {e}"
    
    return test_results


# SECURITY NOTE: disable_network_kill_switch_for_testing function REMOVED
# This was a critical security vulnerability. Kill switches are now PERMANENT.


# Install kill switches immediately when module is imported
logger.info("🔒 Network Kill Switch: ACTIVE - Any network activity will terminate the process")
logger.info(f"🔒 Patched {len(network_kill_switch.original_functions)} network functions")
logger.info("🔒 AI system is now contained - no network access possible")