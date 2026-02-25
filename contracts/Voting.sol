// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Voting {

    address public admin;
    bool public electionActive;

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    mapping(uint => Candidate) public candidates;
    mapping(address => bool) public hasVoted;

    uint public candidateCount;

    constructor() {
        admin = msg.sender;
        electionActive = true;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin allowed");
        _;
    }

    modifier electionOpen() {
        require(electionActive, "Election is closed");
        _;
    }

    function addCandidate(string memory _name) public onlyAdmin {
        candidateCount++;
        candidates[candidateCount] = Candidate(
            candidateCount,
            _name,
            0
        );
    }

    function vote(uint _candidateId) public electionOpen {
        require(!hasVoted[msg.sender], "Already voted");
        require(_candidateId > 0 && _candidateId <= candidateCount, "Invalid candidate");

        hasVoted[msg.sender] = true;
        candidates[_candidateId].voteCount++;
    }

    function endElection() public onlyAdmin {
        electionActive = false;
    }

    function getVotes(uint _candidateId) public view returns (uint) {
        return candidates[_candidateId].voteCount;
    }
}