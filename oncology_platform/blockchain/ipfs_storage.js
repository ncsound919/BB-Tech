/**
 * GenomeOS IPFS Upload Helper
 */
import { NFTStorage } from 'nft.storage';
import crypto from 'crypto';

export async function uploadToGenomeOS(patientData, privateKey) {
    // Step 1: Encrypt Data (AES-256-CBC)
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(privateKey, 'hex'), iv);
    let encrypted = cipher.update(JSON.stringify(patientData));
    encrypted = Buffer.concat([encrypted, cipher.final()]);

    // Step 2: Upload to IPFS
    const client = new NFTStorage({ token: 'API_KEY' });
    const cid = await client.storeBlob(new Blob([encrypted]));
    
    return cid; // Returns the Content Identifier to be stored on Blockchain
}
