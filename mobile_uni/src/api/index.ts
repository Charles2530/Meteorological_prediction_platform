import service from "@/utils/request.ts";

interface ApiResult<T> {
  // `data` 由服务器提供的响应
  data: T;

  // `status` 来自服务器响应的 HTTP 状态码
  status: Number;

  // `statusText` 来自服务器响应的 HTTP 状态信息
  statusText: String;
}

export async function get<T>(url: string, params?: any): Promise<ApiResult<T>> {
  const response = await service.get(url, { params });
  return response;
}
export async function post<T>(url: string, data?: any): Promise<ApiResult<T>> {
  const response = await service.post(url, data);
  return response;
}
export async function put<T>(url: string, data?: any): Promise<ApiResult<T>> {
  const response = await service.put(url, data);
  return response;
}
export async function del<T>(url: string, params?: any): Promise<ApiResult<T>> {
  const response = await service.delete(url, { params });
  return response;
}
