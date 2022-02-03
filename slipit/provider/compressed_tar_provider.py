from __future__ import annotations

import io
import tarfile
from pathlib import Path
from slipit.archive_provider import ArchiveProvider
from slipit.provider.tar_provider import TarProvider


class CompressedTarProvider(TarProvider):
    '''
    ArchiveProvider for tar files.
    '''

    def open(name: str, alg: str = 'gz') -> TarProvider:
        '''
        Open the specified archive.

        Parameters:
            name            file system path of the archive
            alg             compression algorithm

        Returns:
            ArchiveProvider for the opened archive
        '''
        member_content_map = dict()

        if Path(name).is_file():

            with tarfile.open(name, f'r:{alg}') as tar_file:

                for member in tar_file.getmembers():

                    if member.isfile():
                        content = tar_file.extractfile(member).read(member.size)
                        member_content_map[member] = io.BytesIO(content)

                    else:
                        member_content_map[member] = None

        output = tarfile.open(name, f'w:{alg}')

        for member, content in member_content_map.items():
            output.addfile(member, content)

        return TarProvider(output)

    def create(name: str, alg: str) -> TarProvider:
        '''
        Create the specified archive.

        Parameters:
            name            file system path of the archive
            alg             compression algorithm

        Returns:
            ArchiveProvider for the created archive
        '''
        tar_file = tarfile.open(name, f'w:{alg}')
        return TarProvider(tar_file)

    def list_archive(name: str, alg: str = 'gz') -> None:
        '''
        Print a list of the archives content to stdout.

        Parameters:
            name            file system path of the archive
            alg             compression algorithm

        Returns:
            None
        '''
        if not Path(name).is_file():
            raise FileNotFoundError(name)

        with tarfile.open(name, f'r:{alg}') as tar_file:
            tar_file.list()

    def clear_archive(name: str, payload: str, alg: str = 'gz') -> None:
        '''
        Clear the specified archive from all path traversal sequences.

        Parameters:
            name            file system path of the archive
            payload         path traversal payload to look for
            alg             compression algorithm

        Returns:
            None
        '''
        member_content_map = dict()

        if not Path(name).is_file():
            raise FileNotFoundError(name)

        with tarfile.open(name, f'r:{alg}') as tar_file:

            for member in tar_file.getmembers():

                if member.isfile():
                    content = tar_file.extractfile(member).read(member.size)
                    member_content_map[member] = io.BytesIO(content)

                else:
                    member_content_map[member] = None

        with tarfile.open(name, f'w:{alg}') as output:

            for member, content in member_content_map.items():

                if payload not in member.name:
                    output.addfile(member, content)


class GZipProvider(CompressedTarProvider):
    '''
    Archive provider for gzip compressed tar archives.
    '''
    def open(name: str) -> GZipProvider:
        '''
        '''
        return CompressedTarProvider.open(name, 'gz')

    def create(name: str) -> GZipProvider:
        '''
        '''
        return CompressedTarProvider.create(name, 'gz')

    def list_archive(name: str) -> None:
        '''
        '''
        return CompressedTarProvider.list_archive(name, 'gz')

    def clear_archive(name: str, payload: str) -> None:
        '''
        '''
        return CompressedTarProvider.clear_archive(name, payload, 'gz')


class BZip2Provider(CompressedTarProvider):
    '''
    Archive provider for gzip compressed tar archives.
    '''

    def open(name: str) -> BZip2Provider:
        '''
        '''
        return CompressedTarProvider.open(name, 'bz2')

    def create(name: str) -> BZip2Provider:
        '''
        '''
        return CompressedTarProvider.create(name, 'bz2')

    def list_archive(name: str) -> BZip2Provider:
        '''
        '''
        return CompressedTarProvider.list_archive(name, 'bz2')

    def clear_archive(name: str, payload: str) -> BZip2Provider:
        '''
        '''
        return CompressedTarProvider.clear_archive(name, payload, 'bz2')


for ext in ['.gz', '.tgz']:
    ArchiveProvider.register_provider_ext(GZipProvider, ext)

for mime in ['application/gzip', 'application/x-gzip', 'application/x-gtar', 'application/x-tgz']:
    ArchiveProvider.register_provider_mime(GZipProvider, mime)

ArchiveProvider.register_provider_ext(BZip2Provider, '.bz2')
ArchiveProvider.register_provider_mime(BZip2Provider, 'application/x-bzip2')
