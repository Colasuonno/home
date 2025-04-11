import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideStore } from '@ngrx/store';
import {provideHttpClient} from '@angular/common/http';
import {reducers} from './store/app.reducers';
import { provideEffects } from '@ngrx/effects';
import {effects} from './app.effects';

export const homeName = "Casa Colasuonno"
export const homeHost = "localhost"

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }),
    provideHttpClient(),
    provideRouter(routes),
    provideStore(reducers),
    provideEffects(effects),]
};
