import json
import logging
import os

log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(
    level=log_level,
    format='%(asctime)s [%(processName)s] %(levelname)s - %(message)s')
logger = logging.getLogger('Config')

raw_build_paths: list[str] = str(os.environ.get('BUILD_PATHS', '')).split(',')

# If set, only the dockerfiles in these directories wll be used.
# If empty, all the dockerfiles will be detected (Ignore settings take precedence)
build_paths: list[str] = list(filter(None, [path.strip() for path in raw_build_paths]))

# All the docker files in the subdirectories of these root directories will be ignored
ignored_root_dirs: list[str] = json.loads(os.environ.get('IGNORED_ROOT_DIRS', '[]'))

# The dockerfile directly in these directories will be ignored
# (the dockefiles in subdirectories will still be detected)
ignored_components: list[str] = json.loads(os.environ.get('IGNORED_COMPONENTS', '[]'))

# The docker files matching this exact path will be ignored
ignored_paths: list[str] = json.loads(os.environ.get('IGNORED_PATHS', '[]'))

# If the parent directory name is not same as component name, add
# a mapping parent_dir:image_name
name_map: dict[str, str] = json.loads(os.environ.get('NAME_MAP', '{}'))

context_level_map: dict[str, int] = json.loads(
    os.environ.get('CONTEXT_LEVEL_MAP', '{}'))
tag: str = os.environ.get('TAG', '')
image_repository: str = os.environ.get('IMAGE_REPOSITORY', '')
output_file: str = os.environ.get('OUTPUT_FILE', '')
workdir: str = os.environ.get('WORKDIR', '')

logger.debug(f'''Using config -
{log_level=}
{build_paths=}
{ignored_root_dirs=}
{ignored_components=}
{ignored_paths=}
{name_map=}
{context_level_map=}
{tag=}
{image_repository=}
{output_file=}
{workdir=}
''')
