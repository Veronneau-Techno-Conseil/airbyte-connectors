import axios, { AxiosInstance } from "axios"

export class Client{
    private _client: AxiosInstance
    constructor(private baseUrl: string){
        this._client = axios.create({
            baseURL: "https://api.publicapis.org"
        });
    }

    async sample() : Promise<any>{
        console.log("Getting sample");
        return await this._client.get("entries").then(v=>v.data);
    }

    fetch(){
        return this._client.get("entries").then(v=>v.data);
    }

    paged(){

    }
}