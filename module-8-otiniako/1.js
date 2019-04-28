EosApi = require('eosjs-api') // Or EosApi = require('./src')

let options = {
    httpEndpoint: 'http://bp.cryptolions.io:8888', // default, null for cold-storage
    verbose: false, // API logging
    fetchConfiguration: {}
  };

async function doit(options) {
    eos = EosApi(options) // // 127.0.0.1:8888
let produsers = await eos.getProducers({
    'json': true,
    'scope': 'eosio',
    'code': 'eosio',
    'table': 'global',
    'limit': 20
  })
  //console.log(produsers)
  let j = {
    owner: "",
    total_votes: "",
    is_active: 0,
    url: "",
    unpaid_blocks: "",
    last_claim_time: "",
    location: "",
    stakedVotes: "",
    votePercent: ""
  }
  for (i in produsers.rows) {
      // to get staked eos from 
      let timestamp = 946684800000
      let dates = (Date.now() / 1000) - (timestamp / 1000)
      let weight = Math.floor(dates / (86400 * 7)) / 52 // 86400 = seconds per day 24*3600
    let stakedVotes = (produsers.rows[i].total_votes / Math.pow(2, weight) / 10000).toFixed(0)
    // if you want to get the percentage of votes:
    // total_producer_vote_weight is returned from the getProducers call 
    let votePercent = (produsers.rows[i].total_votes / produsers.total_producer_vote_weight * 100).toFixed(2)
    j.owner = produsers.rows[i].owner;
    j.total_votes = produsers.rows[i].total_votes;
    j.is_active = produsers.rows[i].is_active;
    j.url = produsers.rows[i].url;
    j.unpaid_blocks = produsers.rows[i].unpaid_blocks;
    j.last_claim_time = produsers.rows[i].last_claim_time;
    j.location = produsers.rows[i].location;
    j.stakedVotes = stakedVotes;
    j.votePercent = votePercent;
    console.log(j);
  }
}

doit(options)


// Any API call without a callback parameter will print documentation: description,
// parameters, return value, and possible errors.  All methods and documentation
// are created from JSON files in eosjs/json/api/v1..
//eos.getInfo()

// A Promise is returned if a callback is not provided.
//eos.getProducers({}).then(result => console.log(result))
//eos.getBlock(1).then(result => console.log(result))

// For callbacks instead of Promises provide a callback
//callback = (err, res) => {err ? console.error(err) : console.log(res)}

// The server does not expect any parameters only the callback is needed
//eos.getInfo(callback)

// Parameters are added before the callback
//eos.getBlock(1, callback)

// Parameters can be an object
//eos.getBlock({block_num_or_id: 1}, callback)
//eos.getBlock({block_num_or_id: 1}).then(result => console.log(result))