#--web true
"""
API Path: api/my/filemanagement/rename
This action handles renaming files and folders in the file system.
"""
import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main asynchronous function for renaming files and folders.
    
    Expected parameters:
    - old_path (str): Current path of the file/folder
    - new_name (str): New name for the file/folder
    - base_directory (str, optional): Base directory to restrict operations
    
    Returns:
    - success (bool): Whether the operation was successful
    - message (str): Success or error message
    - new_path (str, optional): New path after renaming
    """
    
    try:
        # Extract parameters
        old_path = args.get('old_path')
        new_name = args.get('new_name')
        base_directory = args.get('base_directory', '/tmp/filemanager')
        
        # Validate required parameters
        if not old_path:
            return {
                'success': False,
                'error': 'MISSING_PARAMETER',
                'message': 'old_path parameter is required'
            }
        
        if not new_name:
            return {
                'success': False,
                'error': 'MISSING_PARAMETER',
                'message': 'new_name parameter is required'
            }
        
        # Sanitize and validate paths
        try:
            old_path_obj = Path(base_directory) / old_path.lstrip('/')
            old_path_resolved = old_path_obj.resolve()
            base_path_resolved = Path(base_directory).resolve()
            
            # Security check: ensure the path is within the base directory
            if not str(old_path_resolved).startswith(str(base_path_resolved)):
                return {
                    'success': False,
                    'error': 'SECURITY_VIOLATION',
                    'message': 'Path is outside allowed directory'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': 'INVALID_PATH',
                'message': f'Invalid path format: {str(e)}'
            }
        
        # Validate new name
        if not is_valid_filename(new_name):
            return {
                'success': False,
                'error': 'INVALID_NAME',
                'message': 'New name contains invalid characters'
            }
        
        # Check if source exists
        if not old_path_resolved.exists():
            return {
                'success': False,
                'error': 'FILE_NOT_FOUND',
                'message': f'Source path does not exist: {old_path}'
            }
        
        # Create new path
        new_path_obj = old_path_resolved.parent / new_name
        
        # Check if destination already exists
        if new_path_obj.exists():
            return {
                'success': False,
                'error': 'FILE_EXISTS',
                'message': f'A file or folder with name "{new_name}" already exists'
            }
        
        # Get item information before renaming
        is_directory = old_path_resolved.is_dir()
        old_name = old_path_resolved.name
        
        # Perform the rename operation
        try:
            await rename_async(old_path_resolved, new_path_obj)
            
            # Calculate relative path for response
            relative_new_path = str(new_path_obj.relative_to(base_path_resolved))
            
            logger.info(f"Successfully renamed {old_path} to {new_name}")
            
            return {
                'success': True,
                'message': f'Successfully renamed "{old_name}" to "{new_name}"',
                'old_path': old_path,
                'old_name': old_name,
                'new_path': f'/{relative_new_path}',
                'new_name': new_name,
                'type': 'folder' if is_directory else 'file'
            }
            
        except PermissionError:
            return {
                'success': False,
                'error': 'PERMISSION_DENIED',
                'message': 'Permission denied: cannot rename file/folder'
            }
        except OSError as e:
            return {
                'success': False,
                'error': 'FILESYSTEM_ERROR',
                'message': f'Filesystem error: {str(e)}'
            }
            
    except Exception as e:
        logger.error(f"Unexpected error in rename action: {str(e)}")
        return {
            'success': False,
            'error': 'INTERNAL_ERROR',
            'message': f'Internal server error: {str(e)}'
        }

async def rename_async(old_path: Path, new_path: Path) -> None:
    """
    Asynchronously rename a file or folder.
    """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, os.rename, str(old_path), str(new_path))

def is_valid_filename(filename: str) -> bool:
    """
    Validate filename for security and filesystem compatibility.
    """
    if not filename or filename in ['.', '..']:
        return False
    
    # Check for invalid characters
    invalid_chars = '<>:"/\\|?*'
    if any(char in filename for char in invalid_chars):
        return False
    
    # Check for reserved names on Windows
    reserved_names = [
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    ]
    if filename.upper() in reserved_names:
        return False
    
    # Check length
    if len(filename) > 255:
        return False
    
    return True

# Entry point for Nuvolaris
def main_handler(args):
    """
    Synchronous wrapper for the async main function.
    This is the entry point that Nuvolaris will call.
    """
    return asyncio.run(main(args))

# For local testing
if __name__ == "__main__":
    # Test the function locally
    test_args = {
        'old_path': '/test/old_file.txt',
        'new_name': 'new_file.txt',
        'base_directory': '/tmp/filemanager'
    }
    result = main_handler(test_args)
    print(json.dumps(result, indent=2))