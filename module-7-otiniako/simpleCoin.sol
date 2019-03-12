pragma solidity ^0.4.23;

contract SimpleStorage {
    uint storedData;
    address _account;

    function set(uint x) public {
        storedData = x;
    }

    function get() public view returns (uint){
        return storedData;
    }
    
    function name() public view returns (string){
        return 'SimpleStorage';
    }
    
    function transfer(address account, uint x) public {
        _account = account;
        storedData = x;
    }
    
    function balanceOf(address account) public view returns (uint) {
        return 42;
    }
}