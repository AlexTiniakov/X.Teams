Tasks list:

---------------------------------------------------------------------------------------------
- get chain_id EOS

cleos get info

---------------------------------------------------------------------------------------------
- generate a pair of keys (public private) (eosjs)

let {PrivateKey, PublicKey, Signature, Aes, key_utils, config} = require('eosjs-ecc')

// Create a new random private key
let privateWif
PrivateKey.randomKey().then(privateKey => privateWif = privateKey.toWif())

// Convert to a public key
pubkey = PrivateKey.fromString(privateWif).toPublic().toString()

---------------------------------------------------------------------------------------------
- get all Block Producers (BPs) in the network

https://eosnetworkmonitor.io/
 cleos -u http://api.eosnewyork.io system listproducers -j

---------------------------------------------------------------------------------------------
- install scatter and cleos, create accounts in testnet (find a purse that supports testnet, find a way to create accounts in testnet, get yourself test EOS)

cleos:
brew tap eosio/eosio
brew install eosio
mkdir contracts
cd contracts
keosd &
tail -f nodeos.log
cleos wallet list
brew tap eosio/eosio.cdt
brew install eosio.cdt
cd /Users/mac/contracts
git clone --recursive https://github.com/eosio/eosio.cdt --branch v1.4.1 --single-branch
cd eosio.cdt
./build.sh
sudo ./install.sh
cleos wallet create --to-console
cleos wallet open
cleos wallet list
cleos wallet unlock
PW5JAR8iNR36b3CLmJuJiSPWqSpxWPUBpnhdjwL9AnDyyQGQ48Wf6
cleos wallet list
cleos wallet create_key
Created new private key with a public key of: "EOS7Vy1wnidgkuLymzmXhwzs9uRzza72GYQxpeVyYVnsGmrswpzT6"
cleos wallet import
5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3
cleos create account eosio bob EOS7Vy1wnidgkuLymzmXhwzs9uRzza72GYQxpeVyYVnsGmrswpzT6 
cleos create account eosio alice EOS7Vy1wnidgkuLymzmXhwzs9uRzza72GYQxpeVyYVnsGmrswpzT6
cleos get account alice
cleos wallet list

scatter:
Account name - alexvrubeluk
Owner Public Key - EOS57kn1cP189CNRgfTykoRnRSaQL7aExxMBSwTSZGZY2cbL2hSaD
Active Public Key - 5JLvFMAXCK5DAhgXWpaJvXooMswTMV3hcuTejNC9u9FZN1ZYQQU


---------------------------------------------------------------------------------------------
- find the top 21 (eos system table)

http://eos-bp-votes.dapptools.info/s/api/block-producer-votes-stack-html/1/21
or
cleos -u https://eu.eosdac.io get table eosio eosio voters

or (testnet)
subcommand="get table eosio eosio namebids --key-type i64 --index 2 -r --show-payer"
cleos --url https://jungle2.cryptolions.io:443 ${subcommand}

---------------------------------------------------------------------------------------------
- vote for a pair of BP (copy the result of the action)
cleos --url https://jungle2.cryptolions.io:443 get info
cleos --url https://jungle2.cryptolions.io:443 get account alexvrubeluk
cleos --url https://jungle2.cryptolions.io:443 system listproducers

cleos --url https://jungle2.cryptolions.io:443 system voteproducer approve alexvrubeluk lioninjungle
executed transaction: fcdd8e0fe5cd763d25d7623a1e803a5bbb27e7fb8f798db43cec0be15fd26d0f  120 bytes  399 us
#         eosio <= eosio::voteproducer          {"voter":"alexvrubeluk","proxy":"","producers":["lioninjungle"]}

---------------------------------------------------------------------------------------------
- calculate how much EOS gets per day top 3 BP
582.4370 + 480.8624 + 755.8639 = 1819.1633
---------------------------------------------------------------------------------------------
- find the formula for calculating the vote decay for the account
// to get staked eos from 
    let stakedVotes = (total_votes / this.calcVoteWeight() / 10000).toFixed(0)

    calcVoteWeight () {
      let timestamp = 946684800000
      let dates = (Date.now() / 1000) - (timestamp / 1000)
      let weight = Math.floor(dates / (86400 * 7)) / 52 // 86400 = seconds per day 24*3600
      return Math.pow(2, weight)
    }

    // if you want to get the percentage of votes:
    // total_producer_vote_weight is returned from the getProducers call 
    let votePercent = (total_votes / total_producer_vote_weight * 100).toFixed(2)
---------------------------------------------------------------------------------------------
- create another permission for your own one (copy the result of the action)
cleos -u https://jungle2.cryptolions.io:443 set account permission alexvrubeluk somepermis EOS7SaSGDVVx7DHPnNeXAVKCmxm3N9y6ryvjPxMLKCtcQF6rrmhpB active
executed transaction: 10ca9302211efb352834c2d26f724d36a396991caf654c73330ac7ba6cea2657  160 bytes  277 us
#         eosio <= eosio::updateauth            {"account":"alexvrubeluk","permission":"somepermis","parent":"active","auth":{"threshold":1,"keys":[...
---------------------------------------------------------------------------------------------
- create Block Producer (copy the result of the action)

cleos --url https://jungle2.cryptolions.io:443 system regproducer alexvrubeluk EOS57kn1cP189CNRgfTykoRnRSaQL7aExxMBSwTSZGZY2cbL2hSaD
executed transaction: b03e7e3c75aebaf32f22899d59e7016d0cb16e0114688f7d2072f56ba3c8dd47  144 bytes  366 us
#         eosio <= eosio::regproducer           {"producer":"alexvrubeluk","producer_key":"EOS57kn1cP189CNRgfTykoRnRSaQL7aExxMBSwTSZGZY2cbL2hSaD","u...
---------------------------------------------------------------------------------------------
- API to find the action (get_action) in which the transaction with the voice that you made in the task above
https://api.monitor.jungletestnet.io/v1/chain/get_action
{"account_name":"alexvrubeluk"}

or 
https://api.monitor.jungletestnet.io/#accountInfo:alexvrubeluk 
---------------------------------------------------------------------------------------------
- find the top 10 largest proxies, find the weight of the voice in the top 10 proxies and the weight of the voice in all accounts that vote through a proxy

watch 1.js


///////////////////////////////////////////////////////////////////////////////////////////////
Prepare for the following theoretical questions:


- What is the language of writing smart contracts for EOS
C++

- What is Stake?

- What is a Vote decay?

- Who are Block Producers?

- What is dapps?

- Permission EOS? What are the standard ones?

- What is proxy accounts?
