import {Command} from 'commander';
import {
  AirbyteConfig,
  AirbyteLogger,
  AirbyteSourceBase,
  AirbyteSourceRunner,
  AirbyteSpec,
  AirbyteStreamBase,
} from 'faros-airbyte-cdk';
import VError from 'verror';

import {Builds} from './streams';

/** The main entry point. */
export function mainCommand(): Command {
  const logger = new AirbyteLogger();
  const source = new ExampleSource(logger);
  return new AirbyteSourceRunner(logger, source).mainCommand();
}

/** Example source implementation. */
class ExampleSource extends AirbyteSourceBase {
  async spec(): Promise<AirbyteSpec> {
    let file = require('./resources/spec.json');
    return new AirbyteSpec(file);
  }
  async checkConnection(config: AirbyteConfig): Promise<[boolean, VError]> {
    return [true, undefined];
  }
  streams(config: AirbyteConfig): AirbyteStreamBase[] {
    return [new Builds(this.logger, config)];
  }
}

