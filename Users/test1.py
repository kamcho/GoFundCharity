from deriv_api import DerivAPI
import asyncio
api_token="a5JfuWsC2pWbU5I"
async def api_v():
    api = DerivAPI( app_id=31063)
    authorize = await api.authorize(api_token)

    proposal = await api.proposal({"proposal": 1, "amount": 100, "barrier": "+0.1", "basis": "payout",
                                   "contract_type": "CALL", "currency": "USD", "duration": 60, "duration_unit": "s",
                                   "symbol": "R_100"
    })
    print(proposal)
    source_proposal: Observable = await api.subscribe(
        {"proposal": 1, "amount": 100, "barrier": "+0.1", "basis": "payout",
         "contract_type": "CALL", "currency": "USD", "duration": 60,
         "duration_unit": "s",
         "symbol": "R_100",
         "subscribe": 1
         })
    source_proposal.subscribe(lambda proposal: print(proposal))
    proposal_id = proposal.get('proposal').get('id')
    buy = await api.buy({"buy": proposal_id, "price": 100})
    print(buy)
    response = await api.balance()
    print(response['balance']['balance'])

asyncio.run(api_v())
