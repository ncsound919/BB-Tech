// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GenomeOS_Remission {
    
    struct PatientProfile {
        string encryptedCID; // IPFS Hash of Genomic Data
        bool isRemissionVerified;
        uint256 lastScanDate;
    }
    
    mapping(address => PatientProfile) public patients;
    address public rto_official; // The "Referee" (Doctor/Verifier)

    event RemissionVerified(address patient, uint256 timestamp);

    constructor() {
        rto_official = msg.sender;
    }

    function registerPatient(string memory _cid) public {
        patients[msg.sender].encryptedCID = _cid;
        patients[msg.sender].isRemissionVerified = false;
    }

    function verifyRemission(address _patient) public {
        require(msg.sender == rto_official, "Only RTO/Doctor can verify");
        
        patients[_patient].isRemissionVerified = true;
        patients[_patient].lastScanDate = block.timestamp;
        
        emit RemissionVerified(_patient, block.timestamp);
    }
}
