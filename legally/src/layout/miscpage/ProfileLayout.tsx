"use client";
import AccountDeletion from "@/components/settings/profile/AccountDeletion";
import ContactForm from "@/components/settings/profile/ContactForm";
import DataExport from "@/components/settings/profile/DataExport";
import LogoutButton from "@/components/settings/profile/LogoutButton";
import PasswordChange from "@/components/settings/profile/PasswordChange";
import ProfileInfo from "@/components/settings/profile/ProfileInfo";

export default function ProfileLayout() {
  return (
    <div className="space-y-8 p-6 max-w-2xl mx-auto">
      <ProfileInfo />
      <PasswordChange />
      <DataExport />
      <ContactForm />
      <AccountDeletion />
      <div className="flex justify-end">
        <LogoutButton />
      </div>
    </div>
  );
}