const SALT = new TextEncoder().encode("fom-autosave-v1");
const IV_LEN = 12;
const TAG_LEN = 16;

export async function deriveUserId(code: string): Promise<string> {
	const buf = await crypto.subtle.digest("SHA-512", new TextEncoder().encode(code));
	return Array.from(new Uint8Array(buf))
		.map((b) => b.toString(16).padStart(2, "0"))
		.join("");
}

export async function deriveKey(code: string): Promise<CryptoKey> {
	const raw = await crypto.subtle.importKey(
		"raw",
		new TextEncoder().encode(code),
		"PBKDF2",
		false,
		["deriveKey"]
	);
	return crypto.subtle.deriveKey(
		{ name: "PBKDF2", salt: SALT, iterations: 100_000, hash: "SHA-256" },
		raw,
		{ name: "AES-GCM", length: 256 },
		false,
		["decrypt"]
	);
}

export async function decrypt(data: ArrayBuffer, key: CryptoKey): Promise<ArrayBuffer> {
	const b = new Uint8Array(data);
	if (b.length < IV_LEN + TAG_LEN) throw new Error("Ciphertext too short");
	const iv = b.slice(0, IV_LEN);
	const tag = b.slice(IV_LEN, IV_LEN + TAG_LEN);
	const ct = b.slice(IV_LEN + TAG_LEN);
	// Web Crypto AES-GCM expects ciphertext || tag (tag appended, not prepended)
	const ctWithTag = new Uint8Array(ct.length + TAG_LEN);
	ctWithTag.set(ct);
	ctWithTag.set(tag, ct.length);
	return crypto.subtle.decrypt({ name: "AES-GCM", iv, tagLength: 128 }, key, ctWithTag);
}
