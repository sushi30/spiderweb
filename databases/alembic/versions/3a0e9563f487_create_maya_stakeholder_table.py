"""create maya stakeholder table

Revision ID: 3a0e9563f487
Revises: 
Create Date: 2020-04-15 18:22:32.954726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3a0e9563f487"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "maya_stakeholder",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("AccumulateHoldings", sa.String(), nullable=True),
        sa.Column("AsmachtaDuachMeshubash", sa.String(), nullable=True),
        sa.Column("IsRequiredToReportChange", sa.String(), nullable=True),
        sa.Column("KodSugYeshut", sa.String(), nullable=True),
        sa.Column("HolderOwner", sa.String(), nullable=True),
        sa.Column("CapitalPct", sa.Float(), nullable=True),
        sa.Column("CapitalPct_Dilul", sa.Float(), nullable=True),
        sa.Column("ChangeSincePrevious", sa.Integer(), nullable=True),
        sa.Column("CompanyName", sa.String(), nullable=True),
        sa.Column("CompanyNameEn", sa.String(), nullable=True),
        sa.Column("CompanyUrl", sa.String(), nullable=True),
        sa.Column("CurrentAmount", sa.Integer(), nullable=True),
        sa.Column("Date2", sa.Date(), nullable=True),
        sa.Column("FullName", sa.String(), nullable=True),
        sa.Column("FullNameEn", sa.String(), nullable=True),
        sa.Column("HeaderMisparBaRasham", sa.String(), nullable=True),
        sa.Column("HeaderSemelBursa", sa.String(), nullable=True),
        sa.Column("IsFrontForOthers", sa.String(), nullable=True),
        sa.Column("MaximumRetentionRate", sa.String(), nullable=True),
        sa.Column("MezahehHotem", sa.Integer(), nullable=True),
        sa.Column("MezahehTofes", sa.Integer(), nullable=True),
        sa.Column("MezahehYeshut", sa.String(), nullable=True),
        sa.Column("MinimumRetentionRate", sa.String(), nullable=True),
        sa.Column("MisparNiarErech", sa.Integer(), nullable=True),
        sa.Column("MisparZihui", sa.String(), nullable=False),
        sa.Column("Nationality", sa.String(), nullable=True),
        sa.Column("NeyarotErechReshumim", sa.String(), nullable=True),
        sa.Column("Notes", sa.Text(), nullable=True),
        sa.Column("Position", sa.String(), nullable=True),
        sa.Column("PreviousAmount", sa.Integer(), nullable=True),
        sa.Column("PreviousCompanyNames", sa.String(), nullable=True),
        sa.Column("PumbiLoPumbi", sa.String(), nullable=True),
        sa.Column("StockName", sa.String(), nullable=False),
        sa.Column("SugMisparZihui", sa.String(), nullable=True),
        sa.Column("TreasuryShares", sa.String(), nullable=True),
        sa.Column("VotePower", sa.Float(), nullable=True),
        sa.Column("VotePower_Dilul", sa.Float(), nullable=True),
        sa.Column("company", sa.String(), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=True),
        sa.Column("fix_for", sa.String(), nullable=True),
        sa.Column("fixed_by", sa.String(), nullable=True),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("next_doc", sa.String(), nullable=True),
        sa.Column("prev_doc", sa.String(), nullable=True),
        sa.Column("stakeholder_type", sa.String(), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("MisparZihui", "StockName", "created_at"),
    )


def downgrade():
    op.drop_table("maya_stakeholder")
