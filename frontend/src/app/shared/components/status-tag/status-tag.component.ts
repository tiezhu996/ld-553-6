import { Component, Input } from '@angular/core';

@Component({ standalone: false,
  selector: 'app-status-tag',
  template: `<span class="tag" [class]="tone">{{ value | statusTranslate }}</span>`,
  styles: [`.tag{display:inline-flex;align-items:center;border-radius:999px;padding:4px 9px;font-size:12px;font-weight:700}.green{background:#e4f4eb;color:#0e7c59}.blue{background:#e3edf9;color:#275d9f}.red{background:#f8e6e1;color:#b33b2e}.amber{background:#f6edd9;color:#a66a00}.gray{background:#ecefec;color:#5f6f67}`]
})
export class StatusTagComponent {
  @Input() value = '';
  get tone(): string {
    if (['OPERATING', 'IDLE', 'COMPLETED', 'PAID'].includes(this.value)) return 'green';
    if (['CHARGING', 'ACCEPTED', 'IN_PROGRESS'].includes(this.value)) return 'blue';
    if (['FAULTY', 'DISABLED', 'CANCELLED'].includes(this.value)) return 'red';
    if (['PENDING', 'MAINTENANCE', 'UNPAID'].includes(this.value)) return 'amber';
    return 'gray';
  }
}
