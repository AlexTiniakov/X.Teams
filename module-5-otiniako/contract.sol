pragma solidity ^0.5.4;
/**
 * The Shitcoin contract does this and that...
 */

library SafeMath {
    function safeAdd(uint a, uint b) internal returns (uint c) {
        c = a + b;
        require(c >= a);
    }
    function safeSub(uint a, uint b) internal returns (uint c) {
        require(b <= a);
        c = a - b;
    }
    function safeMul(uint a, uint b) internal returns (uint c) {
        c = a * b;
        require(a == 0 || c / a == b);
    }
    function safeDiv(uint a, uint b) internal returns (uint c) {
        require(b > 0);
        c = a / b;
    }
}

contract Shitcoin {
    using SafeMath for uint;
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);

    mapping(address => uint) _PrivateInvestors;
    mapping(address => uint) _InvestorInWhiteLists;
    mapping(address => uint) _InvestorNotInWhiteLists;

    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;

    // Tocken Summary (300M - for ICO)
    uint constant public    NumberOfTokenCreated = 5*10**8;
    uint constant public    ISOPricePerTokenInCents = 20;
    uint constant public    ETHPriceUsedForCalculatonInCents = 60000;
    uint constant public    ShitcoinTokensPerETH = 3000;
    uint constant public    TheoreticalMarcetCapInCents = 10**10;
    uint constant public    TockenIssuedForISO = 3*10**8;

    // Total token distribution (500M - total)
    uint constant public    Team1 = 8*10**7;
    uint constant public    PublicSales = 30*10**7;
    uint constant public    AdvisorAndPartners = 5*10**7;
    uint constant public    BonusesForEarlyTockenInvestors = 2*10**7;
    uint constant public    ReservedTokens = 5*10**7;

    // Tokens reserved for team and investors (200M - reserved)
    uint constant public    SeedInvestor = 2*10**7;
    uint constant public    Founders = 5*10**7;
    uint constant public    Reserved = 5*10**7;
    uint constant public    Advisors = 5*10**7;
    uint constant public    Team2 = 3*10**7;

    // Token distribution during ICO Rounds
    struct Round {
        string Name; // name of round
        uint Bonuses;  // Bonuses in %
        uint ProjectedSaleInCents; // Prediction of sale
        uint TocenPriceInCents;   // Price for this round
        uint TockenIssued; // amount of tokens in this round
    }

    Round[] public             Rounds;
    
    address public             _owner;
    address public             _admin;
    address public             _portal;

    

	function GreenX (address admin, address portal) public {
		_owner = msg.sender;
		_admin = admin;
		_portal = portal;

    }

	function transfer (address to, uint tokens) public returns (bool success) {
		balances[msg.sender] = balances[msg.sender].safeSub(tokens);
        balances[to] = balances[to].safeAdd(tokens);
        emit Transfer(msg.sender, to, tokens);
        return true;
    }

	function transferFrom(address from, address to, uint tokens) public returns (bool success) {
		balances[from] = balances[from].safeSub(tokens);
        allowed[from][msg.sender] = allowed[from][msg.sender].safeSub(tokens);
        balances[to] = balances[to].safeAdd(tokens);
        emit Transfer(from, to, tokens);
        return true;
    }

    function approve(address spender, uint tokens) public returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        emit Approval(msg.sender, spender, tokens);
        return true;
    }

	function allowance(address tokenOwner, address spender) public view returns (uint remaining) {
        return allowed[tokenOwner][spender];
    }

	function balanceOf(address tokenOwner) public view returns (uint balance) {
        return balances[tokenOwner];
    }

	function () external  {}

	function getCurrentState () public  {}

	function issueTokenForPrivateInvestor () public  {}

	function issueTokenForPresale () public  {}

	function issueTokenForICO () public  {}

	function trackdownInvestedEther () public  {}

	function issueToken () public  {}

	function addToWhitelist (address add) public  {
		require(msg.sender == _owner || msg.sender == _admin || msg.sender == _portal);
		_InvestorInWhiteLists[add] = 1;
	}

	function removeFromWhitelist (address del) public  {
		require(msg.sender == _owner || msg.sender == _admin || msg.sender == _portal);
		_InvestorInWhiteLists[del] = 0;
	}

	function addPrivateInvestor () public  {}

	function removePrivateInvestor () public  {}
	
	function startPrivateSale () public  {}

	function startPreSale () public  {}

	function endPreSale () public  {}
	
	function startICO () public  {}

	function endICO () public  {}

	function setPrivateSalePrice () public  {}

	function setPreSalePrice () public  {}

	function setICOPrice () public  {}

	function revokeToken () public  {}

	function activateContract () public  {}

	function deactivateContract () public  {}

	function enableTokenTransfer () public   {}

	function changeFundKeeper() public  {}

	function changeAdminAddress () public  {}

	function changePortalddress () public   {}

	function changeFounderAddress () public  {}

	function changeTeamAddress () public  {}

	function changeReservedAddress () public  {}
	
	function allocateTokenForFounder () public  {}
}
