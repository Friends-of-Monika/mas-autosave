const ENDPOINT = import.meta.env.VITE_API_ENDPOINT ?? "";

export interface Version {
	sha256: string;
	timestamp: string;
	size: number;
	reason: string;
}

export async function listVersions(userId: string): Promise<Version[]> {
	const res = await fetch(`${ENDPOINT}/saves/${userId}/versions`);
	if (!res.ok) throw new Error(`Server returned ${res.status}`);
	return res.json() as Promise<Version[]>;
}

export async function downloadVersion(userId: string, sha256: string): Promise<ArrayBuffer> {
	const res = await fetch(`${ENDPOINT}/saves/${userId}/${sha256}`);
	if (!res.ok) throw new Error(`Server returned ${res.status}`);
	return res.arrayBuffer();
}
