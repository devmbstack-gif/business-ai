export type LoginResponse = {
  access_token: string;
  token_type: string;
  user_id: number;
  is_guest: boolean;
  is_admin: boolean;
};

export type UserProfile = {
  id: number;
  email: string | null;
  full_name: string | null;
  role: string;
  plan: string;
  is_guest: boolean;
  is_admin: boolean;
  created_at: string;
};
