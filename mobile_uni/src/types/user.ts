export const enum UserRole {
  Visitor = 0,
  User = 1,
  Administrator = 2,
}

export interface UserInfo {
  username: string;
  avatar: string;
  email: string | undefined;
  role: UserRole;
}

export interface UserDetail {
  uid: number;
  username: string;
  avatar: string;
  email: string | undefined;
  role: UserRole;
  last_login: Date;
}
