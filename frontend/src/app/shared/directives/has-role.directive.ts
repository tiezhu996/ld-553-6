import { Directive, Input, TemplateRef, ViewContainerRef } from '@angular/core';
import { UserRole } from '../constants/enums';
import { AuthService } from '../services/auth.service';

@Directive({ standalone: false, selector: '[appHasRole]' })
export class HasRoleDirective {
  constructor(private tpl: TemplateRef<unknown>, private vcr: ViewContainerRef, private auth: AuthService) {}
  @Input() set appHasRole(roles: UserRole[]) {
    this.vcr.clear();
    if (this.auth.hasRole(roles)) this.vcr.createEmbeddedView(this.tpl);
  }
}
