import { Injectable } from '@angular/core';
import { HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private snackBar: MatSnackBar, private auth: AuthService) {}
  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    return next.handle(req).pipe(catchError((error: HttpErrorResponse) => {
      const message = this.messageFor(error);
      this.snackBar.open(message, '关闭', { duration: 3200 });
      if (error.status === 401) this.auth.logout();
      return throwError(() => error);
    }));
  }
  private messageFor(error: HttpErrorResponse): string {
    if (error.status === 0) return '网络连接异常，请检查网络';
    if (error.status === 403) return '无权限执行此操作';
    if (error.status === 404) return '请求的资源不存在';
    if (error.status === 422) return '表单校验失败';
    if (error.status >= 500) return '服务器内部错误';
    return error.error?.message || '请求处理失败';
  }
}
