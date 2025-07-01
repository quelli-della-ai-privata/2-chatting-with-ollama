#--web true
"""
API Path: api/my/filemanagement/delete
This action handles deleting files and folders from the file system.
"""
import os
import json
import asyncio
import shutil
from pathlib import Path
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main asynchronous function for deleting files and folders.
    
    Expected parameters:
    - paths (list): Array of file/folder paths to delete
    - base_directory (str, optional): Base directory to restrict operations
    - force (bool, optional): Force delete non-empty directories
    
    Returns:
    - success (bool): Whether the operation was successful
    - message (str): Success or error message
    - deleted_items (list): List of successfully deleted items
    - failed_items (list): List of items that failed to delete
    """
    
    try:
        # Extract parameters
        paths = args.get('paths', [])
        base_directory = args.get('base_directory', '/tmp/filemanager')
        force = args.get('force', False)
        
        # Validate required parameters
        if not paths:
            return {
                'success': False,
                'error': 'MISSING_PARAMETER',
                'message': 'paths parameter is required'
            }
        
        if not isinstance(paths, list):
            # If single path provided as string, convert to list
            if isinstance(paths, str):
                paths = [paths]
            else:
                return {
                    'success': False,
                    'error': 'INVALID_PARAMETER',
                    'message': 'paths must be an array or string'
                }
        
        # Validate base directory
        try:
            base_path_resolved = Path(base_directory).resolve()
            
            # Ensure base directory exists
            if not base_path_resolved.exists():
                return {
                    'success': False,
                    'error': 'BASE_DIRECTORY_NOT_FOUND',
                    'message': f'Base directory does not exist: {base_directory}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': 'INVALID_BASE_DIRECTORY',
                'message': f'Invalid base directory: {str(e)}'
            }
        
        deleted_items = []
        failed_items = []
        
        # Process each path
        for path in paths:
            try:
                delete_result = await process_single_delete(
                    path, 
                    base_path_resolved,
                    force
                )
                
                if delete_result['success']:
                    deleted_items.append(delete_result)
                else:
                    failed_items.append(delete_result)
                    
            except Exception as e:
                logger.error(f"Error deleting path {path}: {str(e)}")
                failed_items.append({
                    'success': False,
                    'path': path,
                    'error': 'PROCESSING_ERROR',
                    'message': f'Error processing deletion: {str(e)}'
                })
        
        # Determine overall success
        total_items = len(paths)
        successful_deletions = len(deleted_items)
        
        if successful_deletions == total_items:
            message = f'Successfully deleted {successful_deletions} item(s)'
            success = True
        elif successful_deletions > 0:
            message = f'Deleted {successful_deletions} of {total_items} items. {len(failed_items)} failed.'
            success = True  # Partial success
        else:
            message = f'Failed to delete all {total_items} items'
            success = False
        
        logger.info(f"Delete operation completed: {successful_deletions}/{total_items} successful")
        
        return {
            'success': success,
            'message': message,
            'deleted_items': deleted_items,
            'failed_items': failed_items,
            'total_items': total_items,
            'successful_deletions': successful_deletions
        }
        
    except Exception as e:
        logger.error(f"Unexpected error in delete action: {str(e)}")
        return {
            'success': False,
            'error': 'INTERNAL_ERROR',
            'message': f'Internal server error: {str(e)}'
        }

async def process_single_delete(
    path: str,
    base_path: Path,
    force: bool
) -> Dict[str, Any]:
    """
    Process a single file/folder deletion.
    """
    try:
        # Sanitize and validate path
        try:
            target_path_obj = Path(base_path) / path.lstrip('/')
            target_path_resolved = target_path_obj.resolve()
            
            # Security check: ensure the path is within the base directory
            if not str(target_path_resolved).startswith(str(base_path)):
                return {
                    'success': False,
                    'path': path,
                    'error': 'SECURITY_VIOLATION',
                    'message': 'Path is outside allowed directory'
                }
                
        except Exception as e:
            return {
                'success': False,
                'path': path,
                'error': 'INVALID_PATH',
                'message': f'Invalid path format: {str(e)}'
            }
        
        # Check if item exists
        if not target_path_resolved.exists():
            return {
                'success': False,
                'path': path,
                'error': 'ITEM_NOT_FOUND',
                'message': f'Item does not exist: {path}'
            }
        
        # Get item information before deletion
        is_directory = target_path_resolved.is_dir()
        item_name = target_path_resolved.name
        
        # Check if directory is empty (if not forcing)
        if is_directory and not force:
            try:
                # Check if directory has contents
                contents = list(target_path_resolved.iterdir())
                if contents:
                    return {
                        'success': False,
                        'path': path,
                        'error': 'DIRECTORY_NOT_EMPTY',
                        'message': f'Directory "{item_name}" is not empty. Use force=true to delete non-empty directories.'
                    }
            except Exception as e:
                return {
                    'success': False,
                    'path': path,
                    'error': 'DIRECTORY_READ_ERROR',
                    'message': f'Cannot read directory contents: {str(e)}'
                }
        
        try:
            # Perform the delete operation
            if is_directory:
                await delete_directory_async(target_path_resolved)
            else:
                await delete_file_async(target_path_resolved)
            
            logger.info(f"Successfully deleted {'directory' if is_directory else 'file'}: {path}")
            
            return {
                'success': True,
                'path': path,
                'name': item_name,
                'type': 'folder' if is_directory else 'file',
                'message': f'Successfully deleted {"folder" if is_directory else "file"} "{item_name}"'
            }
            
        except PermissionError:
            return {
                'success': False,
                'path': path,
                'error': 'PERMISSION_DENIED',
                'message': f'Permission denied: cannot delete {"directory" if is_directory else "file"}'
            }
        except OSError as e:
            return {
                'success': False,
                'path': path,
                'error': 'FILESYSTEM_ERROR',
                'message': f'Filesystem error: {str(e)}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'path': path,
            'error': 'PROCESSING_ERROR',
            'message': f'Error processing deletion: {str(e)}'
        }

async def delete_file_async(file_path: Path) -> None:
    """
    Asynchronously delete a file.
    """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, os.remove, str(file_path))

async def delete_directory_async(dir_path: Path) -> None:
    """
    Asynchronously delete a directory and all its contents.
    """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, shutil.rmtree, str(dir_path))

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
        'paths': ['/test/file_to_delete.txt'],
        'base_directory': '/tmp/filemanager',
        'force': False
    }
    result = main_handler(test_args)
    print(json.dumps(result, indent=2))