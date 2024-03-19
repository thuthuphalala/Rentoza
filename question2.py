def RebalanceFund(assets, assetCap, totalCapital):
   
    totalMcap = sum(asset['mcap'] for asset in assets)

    initialAllocations = [(asset['mcap'] / totalMcap) for asset in assets]

    adjustedAllocations = []
    remainingCapital = totalCapital
    for allocation in initialAllocations:
        if allocation > assetCap:
            adjustedAllocations.append(assetCap)
            remainingCapital -= assetCap * totalCapital
        else:
            adjustedAllocations.append(allocation)

    if remainingCapital > 0:
        belowCapAssets = [value for value, allocation in enumerate(adjustedAllocations) if allocation < assetCap]
        if belowCapAssets:
            totalBelowCapAllocation = sum(adjustedAllocations[value] for value in belowCapAssets)
            for value in belowCapAssets:
                adjustedAllocations[value] *= remainingCapital / ( totalBelowCapAllocation* totalCapital)

    totalAdjustedAllocation = sum(adjustedAllocations)
    adjustedAllocations = [allocation / totalAdjustedAllocation for allocation in adjustedAllocations]

    results = []
    for asset, allocation in zip(assets, adjustedAllocations):
        amount = allocation * totalCapital / asset['price']
        usdValue = amount * asset['price']
        percentage = allocation * 100
        results.append({
            'amount': amount,
            'usdValue': usdValue,
            'percentage': percentage
        })

    return results

if __name__=="__main__": 
    assets = [
        {'mcap': 20000, 'price': 50},
        {'mcap': 10000, 'price': 25},
        {'mcap': 5000, 'price': 10}
    ]
    assetCap = 0.5          #Change asset cap here
    totalCapital = 1000

    results = RebalanceFund(assets, assetCap, totalCapital)

    for i, result in enumerate(results):
        print(f"Asset {i+1}:")
        print(f"Amount =",round(result['amount'],6))
        print(f"USD value  =",round(result['usdValue'],2))
        print(f"percentage =",round(result['percentage'],4))
        print()