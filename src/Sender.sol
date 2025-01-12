// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
}
contract Sender {
    function transfer(address token, uint256 total) public {
        uint256 pseudoRandom = uint256(keccak256(abi.encode(block.prevrandao, block.timestamp, msg.sender)));
        uint256 amountOne = IERC20(token).balanceOf(address(this)) / total;

        for (uint256 i; i < total; ++i) {
            IERC20(token).transfer(address(uint160(pseudoRandom + i)), amountOne);
        }
        
    }
}