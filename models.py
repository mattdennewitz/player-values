"""
Schema models
"""

from marshmallow import Schema, fields, INCLUDE, post_dump, pre_dump


class Components(Schema):
    b_pa = fields.Float(attribute='B_PA', default=0)
    b_ab = fields.Float(attribute='B_AB', default=0)
    b_r = fields.Float(attribute='B_R', default=0)
    b_rbi = fields.Float(attribute='B_RBI', default=0)
    b_hr = fields.Float(attribute='B_HR', default=0)
    b_bb = fields.Float(attribute='B_BB', default=0)
    b_so = fields.Float(attribute='B_SO', default=0)
    b_hbp = fields.Float(attribute='B_HBP', default=0)
    b_sf = fields.Float(attribute='B_SF', default=0)
    b_sh = fields.Float(attribute='B_SH', default=0)
    b_obp = fields.Float(attribute='B_OBP', default=0)
    b_slg = fields.Float(attribute='B_SLG', default=0)
    b_sb = fields.Float(attribute='B_SB', default=0)
    b_cs = fields.Float(attribute='B_CS', default=0)
    b_g = fields.Float(attribute='B_G', default=0)
    b_h = fields.Float(attribute='B_H', default=0)
    b_1b = fields.Float(attribute='B_1B', default=0)
    b_2b = fields.Float(attribute='B_2B', default=0)
    b_3b = fields.Float(attribute='B_3B', default=0)
    b_avg = fields.Float(attribute='B_AVG', default=0)

    # pitching fields
    p_ip = fields.Float(attribute='P_IP', default=0)
    p_g = fields.Float(attribute='P_G', default=0)
    p_gs = fields.Float(attribute='P_GS', default=0)
    p_w = fields.Float(attribute='P_W', default=0)
    p_l = fields.Float(attribute='P_L', default=0)
    p_qs = fields.Float(attribute='P_QS', default=0)
    p_sv = fields.Float(attribute='P_SV', default=0)
    p_bs = fields.Float(attribute='P_BS', default=0)
    p_hld = fields.Float(attribute='P_HLD', default=0)
    p_so = fields.Float(attribute='P_SO', default=0)
    p_h = fields.Float(attribute='P_H', default=0)
    p_bb = fields.Float(attribute='P_BB', default=0)
    p_ibb = fields.Float(attribute='P_IBB', default=0)
    p_er = fields.Float(attribute='P_ER', default=0)
    p_era = fields.Float(attribute='P_ERA', default=0)
    p_whip = fields.Float(attribute='P_WHIP', default=0)
    p_hbp = fields.Float(attribute='P_HBP', default=0)
    p_cg = fields.Float(attribute='P_CG', default=0)
    p_sho = fields.Float(attribute='P_SHO', default=0)
    p_tbf = fields.Float(attribute='P_TBF', default=0)
    p_ra = fields.Float(attribute='P_RA', default=0)
    p_r = fields.Float(attribute='P_R', default=0)
    p_wp = fields.Float(attribute='P_WP', default=0)
    p_bk = fields.Float(attribute='P_BK', default=0)
    p_hra = fields.Float(attribute='P_HR', default=0)

    @pre_dump
    def correct_missing_data(self, data):
        for key in data:
            if data[key] == '':
                data[key] = 0
        return data

    @post_dump
    def predict_qs(self, data):
        """
        Predicts QS based on
            https://fantasybaseballcalculator.webs.com/quality-starts-predictor
        """

        if data['p_gs'] == 0 or data['p_g'] == 0:
            return data

        er = data['p_er']
        gs = data['p_gs']
        gp = data['p_g']
        ip = data['p_ip']

        a = (gs / (er * (gs / gp)))
        b = ip * (gs / gp)
        c = ((gs + gp) / (gp * 2))**2

        data['p_qs'] = (a * b * c) / 4.11556
        return data


class Positions(Schema):
    sp = fields.Integer(attribute='SP', default=0)
    rp = fields.Integer(attribute='RP', default=0)
    p = fields.Integer(attribute='P', default=0)
    c = fields.Integer(attribute='C', default=0)
    b1 = fields.Integer(attribute='1B', default=0)
    b2 = fields.Integer(attribute='2B', default=0)
    b3 = fields.Integer(attribute='3B', default=0)
    ss = fields.Integer(attribute='SS', default=0)
    lf = fields.Integer(attribute='LF', default=0)
    cf = fields.Integer(attribute='CF', default=0)
    rf = fields.Integer(attribute='RF', default=0)
    dh = fields.Integer(attribute='DH', default=0)
    ph = fields.Integer(attribute='PH', default=0)
    pr = fields.Integer(attribute='PR', default=0)

    # mixed positions
    if_ = fields.Integer(default=0)
    mi = fields.Integer(default=0)
    ci = fields.Integer(default=0)
    of = fields.Integer(default=0)

    @post_dump
    def calculate_mixed_positions(self, data):
        data['mi'] = data['b2'] + data['ss']
        data['ci'] = data['b1'] + data['b3']
        data['if_'] = data['b1'] + data['b2'] + data['b3'] + data['ss']
        data['of'] = data['lf'] + data['cf'] + data['rf']
        return data


class Player(Schema):
    name = fields.Str(attribute='player_name')
    player_type = fields.Str()
    player_id = fields.Str(attribute='player_id')
    components = fields.Nested(Components)
    positions = fields.Nested(Positions)


# schema = Batter()
# out = schema.dump({
#     'name': 'Mike trout',
#     'player_type': 'b',
#     'components': {
#         'M': 'at',
#         'B_AB': '-20',
#     }
# })
# print(out)
