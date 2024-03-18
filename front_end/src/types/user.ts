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

export enum MessageStatus {
  read = 0,
  unread = 1,
}

export enum NotificationType {
  star = 0, // 收藏的课程有新评价
  review = 1, // 评价下有新回复
}

export interface Announcement {
  aid: number;
  title: string;
  content: string;
  datetime: Date;
}

export interface Notification {
  nid: number;
  course_id: number;
  course_name: string;
  review_id: number;
  comment_id?: number;
  datetime: Date;
  status: MessageStatus;
  ntype: NotificationType;
}

export interface UserMessage {
  announcements: Announcement[];
  notifications: Notification[];
}
