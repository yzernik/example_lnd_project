from .rpc_lightning_client import RPCLightningClient


def main():
  client = RPCLightningClient()
  print("Wallet balance:")
  print(client.get_wallet_balance())


if __name__== "__main__":
  main()
