from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalhttp import HttpError

# Creating Access Token for Sandbox
client_id = "AarqWz6bcrYz7vnNFuWFdL9w5PRPg6XsD72AdQrVy9-xGFiMt2nNufHIPxMP1K9otX8pdQVzHl8geOyb"
client_secret = "EJYwTGXDQ4r6RZXlHDJ1chVa5gnqS2zN7FI4DxUgNGhghzavJFyrKZ22shNzvtr0D1991t4aQH5S7SW4"
# Creating an environment
environment = SandboxEnvironment(
    client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)


request = PayoutsPostRequest()


def payout(body):
    request.request_body(body)
    try:
        # Call API with your client and get a response for your call
        response = client.execute(request)
        # If call returns body in response, you can get the deserialized version from the result attribute of the response
        batch_id = response.result.batch_header.payout_batch_id
        print(batch_id)
    except IOError as ioe:
        print(ioe)
        if isinstance(ioe, HttpError):
            # Something went wrong server-side
            print(ioe.status_code)
