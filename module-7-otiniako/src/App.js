import React, { Component } from 'react';
import './App.css';
import Web3 from 'web3'
import Tx from 'ethereumjs-tx'
import secp256k1 from 'secp256k1'
import { PassThrough } from 'stream';


class App extends Component {
  // data = '';
  

  componentWillMount() {
    const ProjectId = '723c0eab8d2e4f30a10fc4a2ce2a08f9'
    //"https://mainnet.infura.io/v3/723c0eab8d2e4f30a10fc4a2ce2a08f9"
    const networks = [
      'http://localhost:7545',
      'https://mainnet.infura.io/v3/'+ProjectId,
      'https://ropsten.infura.io/v3/'+ProjectId,
      'https://rinkeby.infura.io/v3/'+ProjectId,
      'https://kovan.infura.io/v3/'+ProjectId,
      'https://goerli.infura.io/v3/'+ProjectId
    ]
    this.setState({networks: networks.map((number) =>
      <option>{number}</option>)})
    this.loadBlockchainData(null)
  }

  async loadBlockchainData(event) {
    let url;
    if (!event) {
       url = 'http://localhost:7545'
    }
    else {
       url = event.target.value
    }

    const web3 = new Web3(url)
    this.setState({web3})
    //setTimeout(()=>{this.setState({web3})},0
    //const accounts = this.state.users
    //console.log('accounts', accounts)
    //this.setState({accounts: accounts})
  }

  constructor(props) {
    super(props)
    this.state = {
      accounts: '' ,
      networks: '',
      balance: '', 
      web3: Web3, 
      users: [], 
      privkey: '',
      cur_user: '',
      toAddr: '',
      value: '',
      toAddr1: '',
      value1: '',
      contrAddr: '',
      tockens: '',
      cur_tocken: '',
      tockens_to_display: '',
      balanceTocken: '',
      pubkey: '',
      multiWalletAddr: '',
      adresses: [],
      MultiAddrToDisp: '',
      signers: '1',
      //MultiWalAddr: '0x72a31ae048e23ac279089bc9576c9cbe5380f9f8',
      MultiWalAddr: '0xd43343efb0d7951157e6c6e155a9536f454f7d3f',
      MultiWalABI: [
        {
          "constant": false,
          "inputs": [
            {
              "name": "_owners",
              "type": "address[]"
            },
            {
              "name": "_required",
              "type": "uint256"
            }
          ],
          "name": "create",
          "outputs": [
            {
              "name": "wallet",
              "type": "address"
            }
          ],
          "payable": false,
          "stateMutability": "nonpayable",
          "type": "function"
        },
        {
          "anonymous": false,
          "inputs": [
            {
              "indexed": false,
              "name": "sender",
              "type": "address"
            },
            {
              "indexed": false,
              "name": "instantiation",
              "type": "address"
            }
          ],
          "name": "ContractInstantiation",
          "type": "event"
        },
        {
          "constant": true,
          "inputs": [
            {
              "name": "creator",
              "type": "address"
            }
          ],
          "name": "getInstantiationCount",
          "outputs": [
            {
              "name": "",
              "type": "uint256"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        },
        {
          "constant": true,
          "inputs": [
            {
              "name": "",
              "type": "address"
            },
            {
              "name": "",
              "type": "uint256"
            }
          ],
          "name": "instantiations",
          "outputs": [
            {
              "name": "",
              "type": "address"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        },
        {
          "constant": true,
          "inputs": [
            {
              "name": "",
              "type": "address"
            }
          ],
          "name": "isInstantiation",
          "outputs": [
            {
              "name": "",
              "type": "bool"
            }
          ],
          "payable": false,
          "stateMutability": "view",
          "type": "function"
        }
      ]
    }
  }

  render() {
    return (
      <div className="container">
        <h1>BEST WALLET</h1>
        <p>Choose network:  <select onChange={this.loadBlockchainData.bind(this)}>{this.state.networks}</select></p>
        <p>Choose Account: <select onChange={this.changeAddr.bind(this)}>{this.state.accounts}</select></p>
        <p>PublikKey: {this.state.pubkey}</p>
        <p>Balance: {this.state.balance}</p>
        <input type="submit" value='Create new address' onClick={this.newAddr.bind(this)} />
          <p><label> Private key (0x...):<input type="password" name="privkey" value={this.state.privkey}
                            onChange={this.onPasswordChange.bind(this)}/></label><input type="submit" value="Import" onClick={this.importKey.bind(this)}/></p>
        <h3>Send money</h3>
        <p><label> To Address:<input type="text" name="toAddr" value={this.state.toAddr}
                            onChange={this.ontoAddrChange.bind(this)}/></label></p>
        <p><label> Value in eth:<input type="text" name="value" value={this.state.value}
                            onChange={this.onvalueChange.bind(this)}/></label></p>
        <p><input type="submit" value="send" onClick={this.send.bind(this)}/></p>
        <h3>ERC20 tockens</h3>
        <p><label>Add address of tockens:<input type="text" name="value" value={this.state.contrAddr}
                onChange={this.onERC20Change.bind(this)}/></label>
                <input type="submit" value="add" onClick={this.interact_erc20.bind(this)}/></p>
        <p>Choose tocken: <select onChange={this.changeTocken.bind(this)}>{this.state.tockens_to_display}</select></p>
        <p>Balance: {this.state.balanceTocken}</p>

        <h3>Send tockens</h3>
        <p><label> To Address:<input type="text" name="toAddr1" value={this.state.toAddr1}
                            onChange={this.ontoAddr1Change.bind(this)}/></label></p>
        <p><label> Value:<input type="text" name="value1" value={this.state.value1}
                            onChange={this.onvalue1Change.bind(this)}/></label></p>
        <p><input type="submit" value="send" onClick={this.sendTockens.bind(this)}/></p>
        <h3>Multisig Wallet</h3>
        <p><label> Add wallet address:<input type="text" name="multiWalletAddr" value={this.state.multiWalletAddr}
                            onChange={this.onmultiWalletAddrChange.bind(this)}/></label>
                            <input type="submit" value="add Address" onClick={this.addAddressMulti.bind(this)}/></p>

        <p><label> Set number of signers:<input type="text" name="signers" value={this.state.signers}
        onChange={this.onsignersChange.bind(this)}/></label></p>
        <p>Current addresses:</p>{this.state.MultiAddrToDisp}

        <p><input type="submit" value="Create Multisig Wallet" onClick={this.createMultiWallet.bind(this)}/></p>
        
      </div>


    );
  }
onsignersChange(event) {
  this.setState({signers: event.target.value});
}

  onmultiWalletAddrChange(event) {
    this.setState({multiWalletAddr: event.target.value});
  }

  addAddressMulti(event) {
    var adresses = [this.state.multiWalletAddr, ...this.state.adresses]
    this.setState({MultiAddrToDisp: adresses.map((number) =>
      <li>{number}</li>)})
    //var MultiAddrToDisp = [<p>{this.state.multiWalletAddr}</p>, ...this.state.MultiAddrToDisp]
    this.setState({adresses: adresses})
    //this.setState({MultiAddrToDisp: MultiAddrToDisp})
    setTimeout(() => {}, 10)
  }

  createMultiWallet(event) {
    let contract;
    try {
      contract = new this.state.web3.eth.Contract(this.state.MultiWalABI, this.state.MultiWalAddr)//this.state.web3.eth.accounts.privateKeyToAccount(this.state.privkey);
    }
    catch(e)  {
      console.log('error', e);
    }
    try {
      const web3 = this.state.web3
      const account1 = this.state.cur_user.address
      const privkey1 = Buffer.from(this.state.cur_user.privateKey.replace('0x', ''), 'hex')//this.state.cur_user.privateKey)
      console.log('privkey1', privkey1)
      const data = contract.methods.create(this.state.adresses, parseInt(this.state.signers)).encodeABI()
      console.log('this.state.adresses',this.state.adresses)

      web3.eth.getTransactionCount(account1, (err, txCount) => {
      
        //build the transaction
        const txObject = {
          nonce: web3.utils.toHex(txCount),
          gasLimit: web3.utils.toHex(800000),
          gasPrice: web3.utils.toHex(web3.utils.toWei('10', 'gwei')),
          to: this.state.MultiWalAddr,
          data: data
        }
        console.log("txObject", txObject)
        //sign the transaction
        const tx = new Tx(txObject);
        tx.sign(privkey1);
        const serializedTx = tx.serialize();
        const raw = '0x' + serializedTx.toString('hex')

        //broadcast the transaction
        web3.eth.sendSignedTransaction(raw, (err, txHash) => {
          console.log('txHash:', txHash)
        })
      });

      //this.getBal(this.state.cur_user)
      }
    catch(e)  {
      console.log('error', e);
    }
  }

  createProposal(event) {

  }

  signProposal(event) {

  }

  rejectProposal(event) {

  }



  changeTocken(event) {
    const tocken = event.target.value;
    const web3 = this.state.web3
    //console.log("tocken", tocken)
    //const bal1 = this.state.cur_tocken.tocken.methods.balanceOf('0x04cEAb79390F3de7D12C01899E49459fbB86E546').call('0x04cEAb79390F3de7D12C01899E49459fbB86E546');
    //console.log('bal1', bal1)
    this.state.tockens.map((number) => {
      if (number.addr === tocken) {
        console.log(number.addr, tocken)
        this.setState({cur_tocken: number})
        //if (this.state.cur_user != '') {
          console.log("cur_user", this.state.cur_user.address)
          let bal;
          try {
            number.tocken.methods.balanceOf(this.state.cur_user.address, (err, res) => {
              console.log('err:', err, 'res:', res)
              bal = res;
            })
          }
          catch(e)  {
            console.log('error', e);
          }
          
          this.setState({balanceTocken: bal})
          //console.log("bal:", bal)
        //}
      }
    })
  }

  onERC20Change(event) {
    this.setState({contrAddr: event.target.value});
  }

  onPasswordChange(event){
    this.setState({privkey: event.target.value});
  }

  ontoAddrChange(event) {
    this.setState({toAddr: event.target.value})
  }

  onvalueChange(event) {
    this.setState({value: event.target.value})
  }

  ontoAddr1Change(event) {
    this.setState({toAddr1: event.target.value})
  }

  onvalue1Change(event) {
    this.setState({value1: event.target.value})
  }

  send(event) {
    try {
      const web3 = this.state.web3
      const account1 = this.state.cur_user.address
      const account2 = this.state.toAddr
      const privkey1 = Buffer.from(this.state.cur_user.privateKey.replace('0x', ''), 'hex')//this.state.cur_user.privateKey)
      console.log('privkey1', privkey1)


      web3.eth.getTransactionCount(account1, (err, txCount) => {

        //build the transaction
        const txObject = {
          nonce: web3.utils.toHex(txCount),
          to: account2,
          value: web3.utils.toHex(web3.utils.toWei(this.state.value, 'ether')),
          gasLimit: web3.utils.toHex(21000),
          gasPrice: web3.utils.toHex(web3.utils.toWei('10', 'gwei'))
        }

        //sign the transaction
        const tx = new Tx(txObject);
        tx.sign(privkey1);
        const serializedTx = tx.serialize();
        const raw = '0x' + serializedTx.toString('hex')

        //broadcast the transaction
        web3.eth.sendSignedTransaction(raw, (err, txHash) => {
          console.log('txHash:', txHash)
        })
      });

      this.getBal(this.state.cur_user)
      }
    catch(e)  {
      console.log('error', e);
    }
  }

  sendTockens(event) {
    try {
      const web3 = this.state.web3
      const account1 = this.state.cur_user.address
      const account2 = this.state.toAddr1
      const privkey1 = Buffer.from(this.state.cur_user.privateKey.replace('0x', ''), 'hex')//this.state.cur_user.privateKey)
      console.log('privkey1', privkey1)
      const data = this.state.cur_tocken.tocken.methods.transfer(account2, web3.utils.toHex(this.state.value1)).encodeABI()

      web3.eth.getTransactionCount(account1, (err, txCount) => {
      
        //build the transaction
        const txObject = {
          nonce: web3.utils.toHex(txCount),
          gasLimit: web3.utils.toHex(800000),
          gasPrice: web3.utils.toHex(web3.utils.toWei('10', 'gwei')),
          to: this.state.cur_tocken.addr,
          data: data
        }
        console.log("txObject", txObject)
        //sign the transaction
        const tx = new Tx(txObject);
        tx.sign(privkey1);
        const serializedTx = tx.serialize();
        const raw = '0x' + serializedTx.toString('hex')

        //broadcast the transaction
        web3.eth.sendSignedTransaction(raw, (err, txHash) => {
          console.log('txHash:', txHash)
        })
      });

      this.getBal(this.state.cur_user)
      }
    catch(e)  {
      console.log('error', e);
    }

  }

  importKey(event) {
    console.log('privkey',this.state.privkey)
    let account;
    try {
      account = this.state.web3.eth.accounts.privateKeyToAccount(this.state.privkey);
      console.log('account', account);
      var users = [account, ...this.state.users]
      this.setState({users: users})
      var accounts = [<option>{account.address}</option>, ...this.state.accounts]
      this.setState({accounts: accounts})
      this.setState({cur_user: account})
      this.getBal(account)
    }
    catch(e)  {
      console.log('error', e);
    }
    
  }

  getBal(account) {
    const web3 = this.state.web3
    let bal;
    web3.eth.getBalance(account.address, (err, wei) => {
      bal = web3.utils.fromWei(wei, 'ether');
      this.setState({balance: bal})

      
      
      console.log('balance:', bal)
      console.log("1", this.state.cur_user.privateKey);
      setTimeout(() => {}, 10)
      var Wallet = require('ethereumjs-wallet');
      var EthUtil = require('ethereumjs-util');

      // Get a wallet instance from a private key
      console.log("2", this.state.cur_user.privateKey)
      const privateKeyBuffer = Buffer.from(this.state.cur_user.privateKey.replace('0x', ''), 'hex');
      console.log(privateKeyBuffer)
      const wallet = Wallet.fromPrivateKey(privateKeyBuffer);

      // Get a public key
      const publicKey = wallet.getPublicKeyString();
      console.log(publicKey);
      this.setState({pubkey: publicKey})
    })
    
  }

   checkNetwork(event){
     //this.state = { accounts: '' , networks: ''}
     console.log(this.data)
   }
  
   changeAddr(event) {
    const Addr = event.target.value
    //console.log(this.state.web3)
    const web3 = this.state.web3
    console.log("Addr", Addr) 
    let bal;
    web3.eth.getBalance(Addr, (err, wei) => {
      bal = web3.utils.fromWei(wei, 'ether');
      this.setState({balance: bal})
    })
    var accounts = this.state.users
    let us
    accounts.map((number) => {
      
      if (number.address === Addr) {
        us = number
        this.setState({cur_user: number})
      }
    })
    setTimeout(()=>{console.log("cur_user:", this.state.cur_user)},10)
    this.getBal(us)
    //console.log("us:", us)
   }

   newAddr(event) {
    //console.log(event.target.value)
    //const accounts = this.state.accounts
    const web3 = this.state.web3
    var account = web3.eth.accounts.create()
    //accounts.append(account)
    console.log(account)
    var users = [account, ...this.state.users]
    var accounts = [<option>{account.address}</option>, ...this.state.accounts]
    //users.map((user) => {accounts = [<option>{user.address}</option>, ...this.state.accounts]})
    this.setState({users: users})
    this.setState({cur_user: account})
    this.setState({accounts: accounts})
    setTimeout(() => {}, 10)
    this.getBal(account)
    console.log('accounts', this.state.accounts)
    console.log('users', this.state.users)
   }

   async getBalTocken(tocken) {
     if (this.state.cur_user !== '') {
      const bal = await tocken.tocken.methods.balanceOf(this.state.cur_user.address).call()
      this.setState({balanceTocken: bal})
      console.log(bal)
     }
     
   }

   async interact_erc20(event) {
    let abi = require('human-standard-token-abi');
    const addr = this.state.contrAddr
    //var MyContract = this.state.web3.eth.contract(abi);
    if (addr != '') {
      //var myContractInstance = MyContract .at(addr);
      //var owner = myContractInstance .owner.call();
      //console.log("owner: ", owner)
      try {
        const tocken = new this.state.web3.eth.Contract(abi, addr)//this.state.web3.eth.accounts.privateKeyToAccount(this.state.privkey);
        const name = await tocken.methods.name().call()
        console.log('name', name);
        console.log('web3:', this.state.web3)
        var tockens = [{name: name, addr: addr, tocken: tocken}, ...this.state.tockens]
        var cur_tocken = {name: name, addr: addr, tocken: tocken}
        var tockens_to_display = tockens.map((number) => <option>{number.name}</option>)
        this.setState({tockens: tockens})
        this.setState({cur_tocken: cur_tocken})
        this.setState({tockens_to_display: tockens_to_display})
        this.getBalTocken(cur_tocken);
        setTimeout(()=>{},10)
      }
      catch(e)  {
        console.log('error', e);
      }
    }
  
   }
}



export default App;
