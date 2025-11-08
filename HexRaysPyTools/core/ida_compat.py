"""
IDA Pro version compatibility layer
Provides wrappers for API changes between IDA 7.x and IDA 9.x+
"""

import idaapi

# Try to import ida_ida for IDA 9.x+
try:
    import ida_ida
    HAS_IDA_IDA = True
except ImportError:
    HAS_IDA_IDA = False


def get_idati():
    """
    Get the idati (type information library) object.

    IDA 9.0+: Use idaapi.get_idati()
    IDA 7.x: Use idaapi.cvar.idati
    """
    if hasattr(idaapi, 'get_idati'):
        return idaapi.get_idati()
    else:
        return idaapi.cvar.idati


def inf_is_64bit():
    """
    Check if the analyzed binary is 64-bit.

    IDA 9.0+: Use ida_ida.inf_is_64bit()
    IDA 7.x: Use idaapi.get_inf_structure().is_64bit()
    """
    if HAS_IDA_IDA and hasattr(ida_ida, 'inf_is_64bit'):
        return ida_ida.inf_is_64bit()
    else:
        return idaapi.get_inf_structure().is_64bit()


def inf_get_procname():
    """
    Get the processor name.

    IDA 9.0+: Use ida_ida.inf_get_procname()
    IDA 7.x: Use idaapi.cvar.inf.procname
    """
    if HAS_IDA_IDA and hasattr(ida_ida, 'inf_get_procname'):
        return ida_ida.inf_get_procname()
    else:
        return idaapi.cvar.inf.procname
