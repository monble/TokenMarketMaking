// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {Token} from "../src/Token.sol";
import {Sender} from '../src/Sender.sol';

contract CounterTest is Test {
    Token public token;
    address alice;
    Sender public sender;

    function setUp() public {
        alice = makeAddr("alice");
        vm.startPrank(alice);
        token = new Token("Token", "TKN", 1000000000000);
        sender = new Sender();
        vm.stopPrank();
    }

    function test_Transfer() public {
        skip(100);
        sender.transfer(address(token), 1);
    }
}
