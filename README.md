### Token Market Making
##### Smart-contracts and Python script for launch token without purchasing snipers
Every time a token with the best volatility is launched, snipers try to buy this token. To counteract their purchases, 2 functions were implemented: 
1. The ability to buy and sell in one block is disabled, which eliminates the possibility of an MEV Sandwich attack.
2. As well as the ability to instantly block a user who bought a newly created token.
### Main files:
```
../src/Token.sol
```
Smart-Contract ERC20, running Solidity `^0.8.0` with minor improvements.
Codebase for Binance Smart Chain.
1. This code calculates the Uniswap V2 pair:
```solidity
        address tokenA = address(this);
        address tokenB = 0x55d398326f99059fF775485246999027B3197955;
        (address token0, address token1) = tokenA < tokenB ? (tokenA, tokenB) : (tokenB, tokenA);
        pair = address(uint160(uint256(keccak256(abi.encodePacked(
                hex'ff',
                0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73,
                keccak256(abi.encodePacked(token0, token1)),
                hex'00fb7f630766e6a796048ea87d01acd3068e8ff67d078148a3fa3f4a84f69bd5'
            )))));
```
2. This code protects users from MEV Sandwich attacks by preventing the token from being bought and sold in the same block:
```solidity
        if (from != router02 && from != universalRouter && from != pair) {
        require(block.number != lastBlock[from]);
        }
        if (to != router02 && to != universalRouter && to != pair) {
        lastBlock[to] = block.number;
        }
```
##### Token Sender
```
../src/Sender.sol
```
This code does pseudo number generation to get a random address to airdrop the token to a large number of addresses:
```solidity
        uint256 pseudoRandom = uint256(keccak256(abi.encode(block.prevrandao, block.timestamp, msg.sender)));
```
##### Python Script
This script blocking snipers.
```
../main.py
```
To make the script work, fill in the following lines:
```
token_address
```
```
private_key
```
```
whitelist_eoa
```
```
whitelist_contracts
```

### Local deployment and Usage
Install Foundry
```
https://book.getfoundry.sh/
```
To utilize the contracts and deploy to a local testnet, you can build the code in your repo with forge:
```
forge build
```
To test you can test the code in your repo with forge:
```
forge test -vvvv --rpc-url https://ankr.com/bsc
```