import json
import logging
import os
from pathlib import Path
import config as conf

logger = logging.getLogger('Lister')


def get_build_paths() -> list[Path]:
    dockerfile_paths = Path('.').rglob('Dockerfile')
    all_paths: list[Path] = [path for path in dockerfile_paths]
    build_paths: list[Path] = []

    if not conf.build_paths:
        logger.info(f'No build paths specified. Processing all {len(all_paths)} dockerfiles.')
        build_paths = all_paths
    else:
        for path in all_paths:
            if len(path.parts) > 1 and path.parts[-2] in conf.build_paths:
                logger.info(f'Added dockerfile "{path}".')
                build_paths.append(path)
        logger.info(f'{len(build_paths)} dockerfiles found on the specified build paths.')
    return build_paths


def filter_paths(paths: list[Path]) -> list[Path]:
    filtered_paths: list[Path] = []
    for path in paths:
        component_path = str(path.parent)
        component_dir = str(path.parts[-2])
        root_dir = str(path.parts[0])

        if component_path in conf.ignored_paths:
            logger.warning(
                f'The path "{component_path}" is configured as ignored path. Skipping dockerfile.')
        elif component_dir in conf.ignored_components:
            logger.warning(
                f'The component "{component_dir}" is configured as ignored component. Skipping dockerfile.')
        elif root_dir in conf.ignored_root_dirs:
            logger.warning(
                f'The path "{component_path}" is under the ignored root dir "{root_dir}". Skipping dockerfile.')
        else:
            filtered_paths.append(path)
    return filtered_paths


def main():
    if conf.workdir:
        os.chdir(conf.workdir)

    build_params = []
    name_map = conf.name_map
    context_level_map = conf.context_level_map

    build_paths: list[Path] = get_build_paths()

    build_paths = filter_paths(build_paths)

    for path in build_paths:
        component_path = str(path)

        logger.info(f'Processing file "{component_path}"')

        component_dir = str(path.parts[-2])
        component_name = name_map[component_dir
        ] if component_dir in name_map else component_dir
        context_level = context_level_map[component_dir
        ] if component_dir in context_level_map else 1
        context = str(path.parents[context_level])
        dockerfile = '/'.join(path.parts[len(path.parts) - context_level - 1:])
        image = f'{conf.image_repository}/{component_name}:'.lower() + \
                conf.tag

        logger.debug(
            f'{component_dir=}, {component_name=}, {context_level=}, {context=}, {dockerfile=}, {image=}')

        build_params.append({
            'context': context,
            'dockerfile': dockerfile,
            'image': image})
        logger.info('Added successfully')

    mode = 'w' if os.path.exists(conf.output_file) else 'x'

    with open(conf.output_file, mode) as file:
        json.dump(build_params, file)


if __name__ == '__main__':
    main()
