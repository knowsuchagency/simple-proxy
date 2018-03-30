# -*- coding: utf-8 -*-

"""Main module."""
from aiohttp import web
import aiohttp


async def proxy(request: web.Request, url: str) -> web.Response:
    """Proxy request to url and return json result."""
    headers = {key: value
               for key, value in request.headers.items()
               if key != 'Host'}

    request_kwargs = dict(
        data=(await request.content.read()) if request.can_read_body else None,
        params=request.query
    )

    context = request.app.client_session.request(
        request.method,
        url,
        headers=headers,
        **request_kwargs)

    async with context as proxied_server_response:
        json = await proxied_server_response.json()
        response = web.json_response(json)

        return response


async def index(request: web.Request) -> web.Response:
    """
    Forward GET requests to httpbin.org/get and return response
    """
    return await proxy(request, 'http://httpbin.org/anything')


def create_app():
    """Create web application with routes."""
    app = web.Application()

    app.client_session = aiohttp.ClientSession()

    app.add_routes([
        web.route('*', '/', index)
    ])

    return app


if __name__ == '__main__':

    app = create_app()

    web.run_app(app)
