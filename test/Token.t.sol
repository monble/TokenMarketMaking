// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {Token} from "../src/Token.sol";

contract CounterTest is Test {
    Token public token;
    address alice;

    function setUp() public {
        alice = makeAddr("alice");
        vm.startPrank(alice);
        token = new Token("Token", "TKN", 1000000000000);
        vm.stopPrank();
    }

    function test_Blacklist() public {
        skip(100);
        address bob = makeAddr('bob');
        vm.startPrank(alice);
        token.setBlacklist(address(bob));
        vm.stopPrank();
    }
    function testFuzz_Blacklist(address to) public {
        skip(100);
        vm.startPrank(alice);
        token.setBlacklist(address(to));
        vm.stopPrank();
    }
}
