import { Component } from '@angular/core';

@Component({ standalone: false,
  selector: 'app-layout',
  template: `<app-header></app-header><div class="shell"><app-sidebar></app-sidebar><main><router-outlet></router-outlet></main></div>`,
  styles: [`.shell{display:flex}main{flex:1;min-width:0}`]
})
export class LayoutComponent {}
