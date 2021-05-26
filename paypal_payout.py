from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalhttp import HttpError

# Creating Access Token for Sandbox
client_id = "ASOFrSbPHGij0SWOwBghYvXvxp8eWPifcCxTjSJE0MZHVyh3dylfUMyrDxwPTFPCE13BPbIR_45r4ODu"
client_secret = "EPoLvPnWFPOG0A5Dvy6JyhlWyq3o56uiJXH6XCV1aVHcNUlSsyv2drse-fvgLgzW1DNwAode6cNrjkwh"
# Creating an environment LiveEnvironment when ready
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
