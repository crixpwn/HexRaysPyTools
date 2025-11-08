"""
Unit tests for IDA Pro version compatibility layer (ida_compat.py)

These tests verify that the compatibility wrapper functions correctly
handle both IDA 7.x and IDA 9.x+ API differences.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys


class TestIdaCompatIDA7(unittest.TestCase):
    """Test compatibility layer behavior for IDA 7.x"""

    def setUp(self):
        """Set up test environment for IDA 7.x"""
        # Remove any cached imports
        if 'HexRaysPyTools.core.ida_compat' in sys.modules:
            del sys.modules['HexRaysPyTools.core.ida_compat']
        if 'ida_ida' in sys.modules:
            del sys.modules['ida_ida']

    def test_get_idati_ida7(self):
        """Test get_idati() returns idaapi.cvar.idati for IDA 7.x"""
        # Mock idaapi without get_idati function (IDA 7.x)
        mock_idaapi = MagicMock()
        mock_idaapi.cvar = MagicMock()
        mock_idaapi.cvar.idati = Mock(name='mock_idati_7x')

        # Ensure get_idati doesn't exist (IDA 7.x behavior)
        del mock_idaapi.get_idati

        with patch.dict('sys.modules', {'idaapi': mock_idaapi, 'ida_ida': None}):
            # Import after patching
            from HexRaysPyTools.core import ida_compat
            result = ida_compat.get_idati()

            # Verify it returns cvar.idati
            self.assertEqual(result, mock_idaapi.cvar.idati)

    def test_inf_is_64bit_ida7(self):
        """Test inf_is_64bit() uses get_inf_structure() for IDA 7.x"""
        # Mock idaapi for IDA 7.x
        mock_idaapi = MagicMock()
        mock_inf_struct = Mock()
        mock_inf_struct.is_64bit = Mock(return_value=True)
        mock_idaapi.get_inf_structure = Mock(return_value=mock_inf_struct)

        # ida_ida module doesn't exist in IDA 7.x
        with patch.dict('sys.modules', {'idaapi': mock_idaapi, 'ida_ida': None}):
            # Force reimport
            if 'HexRaysPyTools.core.ida_compat' in sys.modules:
                del sys.modules['HexRaysPyTools.core.ida_compat']

            from HexRaysPyTools.core import ida_compat
            result = ida_compat.inf_is_64bit()

            # Verify it called get_inf_structure().is_64bit()
            mock_idaapi.get_inf_structure.assert_called_once()
            self.assertTrue(result)

    def test_inf_get_procname_ida7(self):
        """Test inf_get_procname() uses idaapi.cvar.inf.procname for IDA 7.x"""
        # Mock idaapi for IDA 7.x
        mock_idaapi = MagicMock()
        mock_idaapi.cvar = MagicMock()
        mock_idaapi.cvar.inf = MagicMock()
        mock_idaapi.cvar.inf.procname = "ARM"

        # ida_ida module doesn't exist in IDA 7.x
        with patch.dict('sys.modules', {'idaapi': mock_idaapi, 'ida_ida': None}):
            # Force reimport
            if 'HexRaysPyTools.core.ida_compat' in sys.modules:
                del sys.modules['HexRaysPyTools.core.ida_compat']

            from HexRaysPyTools.core import ida_compat
            result = ida_compat.inf_get_procname()

            # Verify it returns cvar.inf.procname
            self.assertEqual(result, "ARM")


class TestIdaCompatIDA9(unittest.TestCase):
    """Test compatibility layer behavior for IDA 9.x+"""

    def setUp(self):
        """Set up test environment for IDA 9.x+"""
        # Remove any cached imports
        if 'HexRaysPyTools.core.ida_compat' in sys.modules:
            del sys.modules['HexRaysPyTools.core.ida_compat']
        if 'ida_ida' in sys.modules:
            del sys.modules['ida_ida']

    def test_get_idati_ida9(self):
        """Test get_idati() uses idaapi.get_idati() for IDA 9.x+"""
        # Mock idaapi with get_idati function (IDA 9.x+)
        mock_idaapi = MagicMock()
        mock_idati = Mock(name='mock_idati_9x')
        mock_idaapi.get_idati = Mock(return_value=mock_idati)

        with patch.dict('sys.modules', {'idaapi': mock_idaapi, 'ida_ida': MagicMock()}):
            # Force reimport
            if 'HexRaysPyTools.core.ida_compat' in sys.modules:
                del sys.modules['HexRaysPyTools.core.ida_compat']

            from HexRaysPyTools.core import ida_compat
            result = ida_compat.get_idati()

            # Verify it called idaapi.get_idati()
            mock_idaapi.get_idati.assert_called_once()
            self.assertEqual(result, mock_idati)

    def test_inf_is_64bit_ida9(self):
        """Test inf_is_64bit() uses ida_ida.inf_is_64bit() for IDA 9.x+"""
        # Mock ida_ida for IDA 9.x+
        mock_ida_ida = MagicMock()
        mock_ida_ida.inf_is_64bit = Mock(return_value=False)

        mock_idaapi = MagicMock()

        with patch.dict('sys.modules', {'idaapi': mock_idaapi, 'ida_ida': mock_ida_ida}):
            # Force reimport
            if 'HexRaysPyTools.core.ida_compat' in sys.modules:
                del sys.modules['HexRaysPyTools.core.ida_compat']

            from HexRaysPyTools.core import ida_compat
            result = ida_compat.inf_is_64bit()

            # Verify it called ida_ida.inf_is_64bit()
            mock_ida_ida.inf_is_64bit.assert_called_once()
            self.assertFalse(result)

    def test_inf_get_procname_ida9(self):
        """Test inf_get_procname() uses ida_ida.inf_get_procname() for IDA 9.x+"""
        # Mock ida_ida for IDA 9.x+
        mock_ida_ida = MagicMock()
        mock_ida_ida.inf_get_procname = Mock(return_value="x86")

        mock_idaapi = MagicMock()

        with patch.dict('sys.modules', {'idaapi': mock_idaapi, 'ida_ida': mock_ida_ida}):
            # Force reimport
            if 'HexRaysPyTools.core.ida_compat' in sys.modules:
                del sys.modules['HexRaysPyTools.core.ida_compat']

            from HexRaysPyTools.core import ida_compat
            result = ida_compat.inf_get_procname()

            # Verify it called ida_ida.inf_get_procname()
            mock_ida_ida.inf_get_procname.assert_called_once()
            self.assertEqual(result, "x86")


class TestIdaCompatReturnTypes(unittest.TestCase):
    """Test that compatibility functions return correct types"""

    def test_get_idati_returns_object(self):
        """Test get_idati() returns an object (not None)"""
        mock_idaapi = MagicMock()
        mock_idati = Mock(name='test_idati')
        mock_idaapi.get_idati = Mock(return_value=mock_idati)

        with patch.dict('sys.modules', {'idaapi': mock_idaapi, 'ida_ida': MagicMock()}):
            if 'HexRaysPyTools.core.ida_compat' in sys.modules:
                del sys.modules['HexRaysPyTools.core.ida_compat']

            from HexRaysPyTools.core import ida_compat
            result = ida_compat.get_idati()

            self.assertIsNotNone(result)

    def test_inf_is_64bit_returns_bool(self):
        """Test inf_is_64bit() returns boolean"""
        mock_ida_ida = MagicMock()
        mock_ida_ida.inf_is_64bit = Mock(return_value=True)

        with patch.dict('sys.modules', {'idaapi': MagicMock(), 'ida_ida': mock_ida_ida}):
            if 'HexRaysPyTools.core.ida_compat' in sys.modules:
                del sys.modules['HexRaysPyTools.core.ida_compat']

            from HexRaysPyTools.core import ida_compat
            result = ida_compat.inf_is_64bit()

            self.assertIsInstance(result, bool)

    def test_inf_get_procname_returns_string(self):
        """Test inf_get_procname() returns string"""
        mock_ida_ida = MagicMock()
        mock_ida_ida.inf_get_procname = Mock(return_value="MIPS")

        with patch.dict('sys.modules', {'idaapi': MagicMock(), 'ida_ida': mock_ida_ida}):
            if 'HexRaysPyTools.core.ida_compat' in sys.modules:
                del sys.modules['HexRaysPyTools.core.ida_compat']

            from HexRaysPyTools.core import ida_compat
            result = ida_compat.inf_get_procname()

            self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
