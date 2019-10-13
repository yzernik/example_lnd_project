from typing import Optional

import codecs
import logging
import requests
import json
import grpc
import os

import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc


logger = logging.getLogger(__name__)

# Follow the code from here: https://dev.lightning.community/guides/python-grpc/

# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handhsake
# error when we communicate with the lnd rpc server.
os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'
os.environ["GRPC_VERBOSITY"] = 'debug'

# Lnd cert is at ~/.lnd/tls.cert on Linux and
# ~/Library/Application Support/Lnd/tls.cert on Mac
cert = open(os.path.expanduser('/lnd/.lnd/tls.cert'), 'rb').read()
creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('lnd:10009', creds)
stub = lnrpc.LightningStub(channel)


# Lnd admin macaroon is at ~/.lnd/data/chain/bitcoin/simnet/admin.macaroon on Linux and
# ~/Library/Application Support/Lnd/data/chain/bitcoin/simnet/admin.macaroon on Mac
with open(os.path.expanduser('/lnd/.lnd/data/chain/bitcoin/testnet/admin.macaroon'), 'rb') as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, 'hex')


class RPCLightningClient:
    """Access a lightning deamon using RPC."""

    def get_wallet_balance(self):
        # Retrieve and display the wallet balance
        response = stub.WalletBalance(ln.WalletBalanceRequest(), metadata=[('macaroon', macaroon)])
        return response.total_balance
