import asyncio
import time

import aiohttp
import pytest


async def go(cont: str, name: str):
    conn = aiohttp.UnixConnector(path=r'/var/run/docker.sock')
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(f'http://xx/containers/{cont}/logs?follow=1&stdout=1', ) as resp:
            async for line in resp.content:
                print(name, line)


@pytest.fixture()
async def docker_containers():
    cont1 = 'cont1'
    cont2 = 'cont2'
    name1 = 'vlad'
    name2 = 'sanya'

    await asyncio.create_subprocess_shell(
        f'docker run -d --name {cont1} ubuntu bash -c "echo [INFO] hello world"'
    )
    await asyncio.create_subprocess_shell(
        f'docker run -d --name {cont2} ubuntu bash -c "echo [INFO] foobar"'
    )

    time.sleep(3)

    yield [cont1, cont2, name1, name2]

    await asyncio.create_subprocess_shell(f'docker rm {cont1}')
    await asyncio.create_subprocess_shell(f'docker rm {cont2}')

    yield 0


@pytest.mark.asyncio
async def test_logs(docker_containers, capsys):

    cont1, cont2, name1, name2 = await anext(docker_containers)

    expected_output = [
        f"vlad b'\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x13[INFO] hello world\\n'",
        f"sanya b'\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x0e[INFO] foobar\\n'",
        ''
    ]

    await go(cont1, name1)
    await go(cont2, name2)

    captured = capsys.readouterr()

    actual_output = captured.out.split('\n')
    print(actual_output)

    await anext(docker_containers)

    assert expected_output == actual_output