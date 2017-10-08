from . import app
from flask import abort, request
import socket


def resolve_dns(domain_name):
    try:
        return socket.gethostbyname(domain_name)
    except socket.gaierror as e:
        return None


def whitelist_ips():
    return (ip
            for ip in (resolve_dns(dns) for dns in app.config['DNS_WHITELIST'])
            if ip is not None)


@app.before_request
def limit_remote_addr():
    # TODO: whitelist pivotal urls
    if False and request.remote_addr not in whitelist_ips():
        app.logger.warning('remote_addr(%s) not whitelisted. whitelist: %r',
                           request.remote_addr, list(whitelist_ips()))
        abort(403)

    app.logger.info('request accepted from %s', request.remote_addr)
