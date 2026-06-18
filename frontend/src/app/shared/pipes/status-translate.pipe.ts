import { Pipe, PipeTransform } from '@angular/core';

const labels: Record<string, string> = {
  OPERATING: '运营中', MAINTENANCE: '维修中', DISABLED: '停用', PENDING: '待审核',
  IDLE: '空闲', CHARGING: '充电中', FAULTY: '故障',
  ACCEPTED: '已接单', IN_PROGRESS: '进行中', COMPLETED: '已完成', CANCELLED: '已取消',
  UNPAID: '未支付', PAID: '已支付', REFUNDED: '已退款'
};

@Pipe({ standalone: false, name: 'statusTranslate' })
export class StatusTranslatePipe implements PipeTransform {
  transform(value: string | undefined): string { return value ? (labels[value] || value) : '-'; }
}
