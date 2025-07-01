#--web true
"""
API Path: api/my/filemanagement/search
This action handles searching files and folders in the file system.
"""
import os
import json
import asyncio
import fnmatch
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main asynchronous function for searching files and folders.
    
    Expected parameters:
    - query (str): Search query (filename pattern or text content)
    - search_path (str, optional): Path to search in (default: root)
    - base_directory (str, optional): Base directory to restrict operations
    - search_type (str, optional): 'name' or 'content' or 'both' (default: 'name')
    - include_folders (bool, optional): Include folders in results (default: True)
    - case_sensitive (bool, optional): Case sensitive search (default: False)
    - max_results (int, optional): Maximum number of results (default: 100)
    - file_extensions (list, optional): Filter by file extensions
    
    Returns:
    - success (bool): Whether the operation was successful
    - message (str): Success or error message
    - results (list): List of matching files/folders
    - total_found (int): Total number of items found
    """
    
    try:
        # Extract parameters
        query = args.get('query', '').strip()
        search_path = args.get('search_path', '/')
        base_directory = args.get('base_directory', '/tmp/filemanager')
        search_type = args.get('search_type', 'name').lower()
        include_folders = args.get('include_folders', True)
        case_sensitive = args.get('case_sensitive', False)
        max_results = args.get('max_results', 100)
        file_extensions = args.get('file_extensions', [])
        
        # Validate required parameters
        if not query:
            return {
                'success': False,
                'error': 'MISSING_PARAMETER',
                'message': 'query parameter is required'
            }
        
        # Validate search type
        if search_type not in ['name', 'content', 'both']:
            return {
                'success': False,
                'error': 'INVALID_PARAMETER',
                'message': 'search_type must be "name", "content", or "both"'
            }
        
        # Sanitize and validate search path
        try:
            search_path_obj = Path(base_directory) / search_path.lstrip('/')
            search_path_resolved = search_path_obj.resolve()
            base_path_resolved = Path(base_directory).resolve()
            
            # Security check: ensure the path is within the base directory
            if not str(search_path_resolved).startswith(str(base_path_resolved)):
                return {
                    'success': False,
                    'error': 'SECURITY_VIOLATION',
                    'message': 'Search path is outside allowed directory'
                }
            
            # Check if search path exists
            if not search_path_resolved.exists():
                return {
                    'success': False,
                    'error': 'PATH_NOT_FOUND',
                    'message': f'Search path does not exist: {search_path}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': 'INVALID_PATH',
                'message': f'Invalid search path: {str(e)}'
            }
        
        # Normalize file extensions
        if file_extensions and not isinstance(file_extensions, list):
            file_extensions = [file_extensions]
        
        # Normalize extensions (ensure they start with '.')
        if file_extensions:
            file_extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in file_extensions]
        
        # Perform the search
        try:
            search_results = await perform_search(
                query=query,
                search_path=search_path_resolved,
                base_path=base_path_resolved,
                search_type=search_type,
                include_folders=include_folders,
                case_sensitive=case_sensitive,
                max_results=max_results,
                file_extensions=file_extensions
            )
            
            total_found = len(search_results)
            
            logger.info(f"Search completed: found {total_found} results for query '{query}'")
            
            return {
                'success': True,
                'message': f'Found {total_found} result(s) for "{query}"',
                'results': search_results,
                'total_found': total_found,
                'query': query,
                'search_type': search_type,
                'search_path': search_path
            }
            
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            return {
                'success': False,
                'error': 'SEARCH_ERROR',
                'message': f'Error during search: {str(e)}'
            }
            
    except Exception as e:
        logger.error(f"Unexpected error in search action: {str(e)}")
        return {
            'success': False,
            'error': 'INTERNAL_ERROR',
            'message': f'Internal server error: {str(e)}'
        }

async def perform_search(
    query: str,
    search_path: Path,
    base_path: Path,
    search_type: str,
    include_folders: bool,
    case_sensitive: bool,
    max_results: int,
    file_extensions: List[str]
) -> List[Dict[str, Any]]:
    """
    Perform the actual search operation.
    """
    results = []
    processed_count = 0
    
    # Prepare query for matching
    search_query = query if case_sensitive else query.lower()
    
    try:
        # Walk through the directory tree
        for root, dirs, files in os.walk(search_path):
            # Stop if we've reached max results
            if len(results) >= max_results:
                break
            
            root_path = Path(root)
            
            # Search in folders if requested
            if include_folders:
                for folder_name in dirs:
                    if len(results) >= max_results:
                        break
                    
                    folder_path = root_path / folder_name
                    
                    # Check if folder name matches
                    if search_type in ['name', 'both']:
                        if matches_pattern(folder_name, search_query, case_sensitive):
                            result = await create_search_result(
                                folder_path, base_path, 'folder', query, 'name'
                            )
                            if result:
                                results.append(result)
            
            # Search in files
            for file_name in files:
                if len(results) >= max_results:
                    break
                
                file_path = root_path / file_name
                
                # Filter by file extensions if specified
                if file_extensions:
                    file_ext = file_path.suffix.lower()
                    if file_ext not in file_extensions:
                        continue
                
                # Check filename match
                name_match = False
                if search_type in ['name', 'both']:
                    if matches_pattern(file_name, search_query, case_sensitive):
                        name_match = True
                        result = await create_search_result(
                            file_path, base_path, 'file', query, 'name'
                        )
                        if result:
                            results.append(result)
                            if search_type == 'name':
                                continue  # Skip content search if only searching names
                
                # Check content match (only for text files and if not already matched by name)
                if search_type in ['content', 'both'] and not name_match:
                    try:
                        if await is_text_file(file_path) and await search_file_content(file_path, search_query, case_sensitive):
                            result = await create_search_result(
                                file_path, base_path, 'file', query, 'content'
                            )
                            if result:
                                results.append(result)
                    except Exception as e:
                        logger.warning(f"Error searching content in {file_path}: {str(e)}")
                        continue
                
                processed_count += 1
        
        logger.info(f"Processed {processed_count} files, found {len(results)} matches")
        return results
        
    except Exception as e:
        logger.error(f"Error during directory walk: {str(e)}")
        raise

async def create_search_result(
    file_path: Path, 
    base_path: Path, 
    item_type: str, 
    query: str, 
    match_type: str
) -> Optional[Dict[str, Any]]:
    """
    Create a search result dictionary for a matching item.
    """
    try:
        # Get file stats
        stat = file_path.stat()
        
        # Calculate relative path
        relative_path = str(file_path.relative_to(base_path))
        
        result = {
            'id': str(hash(str(file_path))),  # Simple ID generation
            'name': file_path.name,
            'path': f'/{relative_path}',
            'type': item_type,
            'match_type': match_type,  # 'name' or 'content'
            'size': stat.st_size if item_type == 'file' else None,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'parent_path': str(file_path.parent.relative_to(base_path)) if file_path.parent != base_path else '/'
        }
        
        # Add file extension for files
        if item_type == 'file':
            result['extension'] = file_path.suffix.lower()
        
        return result
        
    except Exception as e:
        logger.warning(f"Error creating search result for {file_path}: {str(e)}")
        return None

def matches_pattern(filename: str, query: str, case_sensitive: bool) -> bool:
    """
    Check if filename matches the search pattern.
    """
    search_name = filename if case_sensitive else filename.lower()
    
    # Support wildcard patterns
    if '*' in query or '?' in query:
        return fnmatch.fnmatch(search_name, query)
    else:
        # Simple substring match
        return query in search_name

async def is_text_file(file_path: Path, max_check_bytes: int = 1024) -> bool:
    """
    Check if a file is likely a text file by examining its content.
    """
    try:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _is_text_file_sync, file_path, max_check_bytes)
    except Exception:
        return False

def _is_text_file_sync(file_path: Path, max_check_bytes: int) -> bool:
    """
    Synchronous version of text file check.
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(max_check_bytes)
            
        # Check for null bytes (binary indicator)
        if b'\x00' in chunk:
            return False
        
        # Try to decode as UTF-8
        try:
            chunk.decode('utf-8')
            return True
        except UnicodeDecodeError:
            # Try other common encodings
            for encoding in ['latin-1', 'cp1252']:
                try:
                    chunk.decode(encoding)
                    return True
                except UnicodeDecodeError:
                    continue
            return False
            
    except Exception:
        return False

async def search_file_content(file_path: Path, query: str, case_sensitive: bool) -> bool:
    """
    Search for query within file content.
    """
    try:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _search_file_content_sync, file_path, query, case_sensitive)
    except Exception as e:
        logger.warning(f"Error searching content in {file_path}: {str(e)}")
        return False

def _search_file_content_sync(file_path: Path, query: str, case_sensitive: bool) -> bool:
    """
    Synchronous version of file content search.
    """
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    search_content = content if case_sensitive else content.lower()
                    return query in search_content
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"Error reading {file_path} with {encoding}: {str(e)}")
                continue
        
        return False
        
    except Exception as e:
        logger.warning(f"Error in content search for {file_path}: {str(e)}")
        return False

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
        'query': '*.txt',
        'search_path': '/',
        'base_directory': '/tmp/filemanager',
        'search_type': 'name',
        'max_results': 50
    }
    result = main_handler(test_args)
    print(json.dumps(result, indent=2))