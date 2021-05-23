from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalhttp import HttpError

# Creating Access Token for Sandbox
client_id = "ATxmnk80cPKjOX0vnD52zBfqxy5415Emu9jfZslayMiOsKWl6a0UVs2vIQjFCNdOUrc3ElejyRjw1JaU"
client_secret = "EPkxfW8RyIc2IA1Si0zsXh2REwEJvLjxUwCVmTB32UoiICStIIhdX12aV4s3F7NoT6haDySwE1rASdtL"
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
