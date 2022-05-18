import deasync from 'deasync';
import {AirbyteConfig, AirbyteLogger, AirbyteStreamBase, StreamKey, SyncMode} from 'faros-airbyte-cdk';
import {Dictionary} from 'ts-essentials';
import { Client } from './client';
import { createSchema } from "genson-js"
import jsonata from "jsonata"
import { syncPromise } from './helper';

export class Builds extends AirbyteStreamBase {
  client: Client
  selector: string
  constructor(logger: AirbyteLogger, private config: AirbyteConfig){
    super(logger);
    this.client = new Client(config["server_url"]);
    this.selector = config["resultSelector"];
  }

  getJsonSchema(): Dictionary<any, string> {
    let o = syncPromise(this.client.sample());
    if(this.selector)
      o = jsonata(this.selector).evaluate(o);
    return createSchema(o);
  }
  
  get name(): string
  {
    return this.config["name"] ?? "request";
  }

  get primaryKey(): StreamKey {
    return '';
  }
  get cursorField(): string | string[] {
    return 'ignore';
  }

  async *readRecords(
    syncMode: SyncMode,
    cursorField?: string[],
    streamSlice?: Dictionary<any, string>,
    streamState?: Dictionary<any, string>
  ): AsyncGenerator<Dictionary<any, string>, any, unknown> {
       
    let res = await this.client.fetch();
    
    if(this.selector)
      res = jsonata(this.selector).evaluate(res);

    if(res instanceof Array){
      var arr = res as Array<any>
      for(var item of arr)
      {
        yield item;
      }
    }
    else{
      yield res;
    }
  }

  
  getUpdatedState(
    currentStreamState: Dictionary<any>,
    latestRecord: Dictionary<any>
  ): Dictionary<any> {
    return {};
  }
}
