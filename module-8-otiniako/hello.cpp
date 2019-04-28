#include <eosiolib/eosio.hpp>

using namespace eosio;

class [[eosio::contract("hello")]] hello : public contract {
  public:
      using contract::contract;

      [[eosio::action]]
      void hi( name user, int i ) {
         print( "Hello, ", name{user}, i % 2 ? ", you win!" : " you lose!");
      }
};

EOSIO_DISPATCH( hello, (hi))