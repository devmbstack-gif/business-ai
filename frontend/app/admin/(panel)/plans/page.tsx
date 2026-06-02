"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api-client";
import { Plan, PlanUpdatePayload } from "@/types/admin";
import { AdminHeader } from "@/components/admin/header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { PageLoader } from "@/components/ui/loading";

type EditState = {
  name: string;
  description: string;
  price_monthly: string;
  analyses_limit: string;
  proposals_limit: string;
  is_active: boolean;
};

export default function AdminPlansPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState<EditState | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  function loadPlans() {
    apiRequest<Plan[]>("/admin/plans")
      .then(setPlans)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    loadPlans();
  }, []);

  function startEdit(plan: Plan) {
    setEditingId(plan.id);
    setEditForm({
      name: plan.name,
      description: plan.description || "",
      price_monthly: String(plan.price_monthly),
      analyses_limit: String(plan.analyses_limit),
      proposals_limit: String(plan.proposals_limit),
      is_active: plan.is_active,
    });
  }

  function cancelEdit() {
    setEditingId(null);
    setEditForm(null);
  }

  async function savePlan(planId: number) {
    if (!editForm) return;
    setSaving(true);
    setError("");

    const payload: PlanUpdatePayload = {
      name: editForm.name,
      description: editForm.description || undefined,
      price_monthly: parseFloat(editForm.price_monthly),
      analyses_limit: parseInt(editForm.analyses_limit, 10),
      proposals_limit: parseInt(editForm.proposals_limit, 10),
      is_active: editForm.is_active,
    };

    try {
      await apiRequest<Plan>(`/admin/plans/${planId}`, {
        method: "PATCH",
        body: payload,
      });
      cancelEdit();
      loadPlans();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update plan");
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <PageLoader />;

  return (
    <div>
      <AdminHeader title="Plans" subtitle="Manage subscription plans" />

      {error && (
        <div className="mb-4 rounded-lg bg-brand-danger/10 px-4 py-3 text-sm text-brand-danger">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {plans.map((plan) => {
          const isEditing = editingId === plan.id;

          return (
            <Card key={plan.id} className={plan.slug === "pro" ? "border-brand-primary/30 ring-1 ring-brand-primary/10" : ""}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>{isEditing ? "Edit Plan" : plan.name}</CardTitle>
                  <Badge variant={plan.is_active ? "success" : "muted"}>
                    {plan.is_active ? "Active" : "Inactive"}
                  </Badge>
                </div>
                {!isEditing && (
                  <p className="mt-1 text-sm capitalize text-brand-text-muted">{plan.slug} plan</p>
                )}
              </CardHeader>

              <CardBody>
                {isEditing && editForm ? (
                  <div className="space-y-4">
                    <Input
                      label="Name"
                      value={editForm.name}
                      onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                    />
                    <Input
                      label="Description"
                      value={editForm.description}
                      onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
                    />
                    <Input
                      label="Price ($/month)"
                      type="number"
                      value={editForm.price_monthly}
                      onChange={(e) => setEditForm({ ...editForm, price_monthly: e.target.value })}
                    />
                    <Input
                      label="Analyses Limit"
                      type="number"
                      value={editForm.analyses_limit}
                      onChange={(e) => setEditForm({ ...editForm, analyses_limit: e.target.value })}
                    />
                    <Input
                      label="Proposals Limit"
                      type="number"
                      value={editForm.proposals_limit}
                      onChange={(e) => setEditForm({ ...editForm, proposals_limit: e.target.value })}
                    />
                    <label className="flex items-center gap-2 text-sm text-brand-text">
                      <input
                        type="checkbox"
                        checked={editForm.is_active}
                        onChange={(e) => setEditForm({ ...editForm, is_active: e.target.checked })}
                        className="rounded border-brand-border"
                      />
                      Active
                    </label>
                    <div className="flex gap-2 pt-2">
                      <Button size="sm" loading={saving} onClick={() => savePlan(plan.id)}>
                        Save
                      </Button>
                      <Button size="sm" variant="outline" onClick={cancelEdit}>
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div>
                    <p className="text-3xl font-bold text-brand-text">
                      ${plan.price_monthly}
                      <span className="text-sm font-normal text-brand-text-muted">/mo</span>
                    </p>
                    {plan.description && (
                      <p className="mt-2 text-sm text-brand-text-muted">{plan.description}</p>
                    )}
                    <div className="mt-4 space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-brand-text-muted">Analyses</span>
                        <span className="font-medium text-brand-text">{plan.analyses_limit}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-brand-text-muted">Proposals</span>
                        <span className="font-medium text-brand-text">{plan.proposals_limit}</span>
                      </div>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      className="mt-5 w-full"
                      onClick={() => startEdit(plan)}
                    >
                      Edit Plan
                    </Button>
                  </div>
                )}
              </CardBody>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
