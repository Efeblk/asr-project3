"""Kazakh/Russian transcript filter (rule 3). Examples are real KSC2-style lines audited by hand."""

from asrbench.langfilter import CharNB, label

KK = ["жергілікті тұрғындар құрылыс тежелмей жедел іске асса деп отыр", "осыдан жиырма жыл бұрын болған",
      "қала тұрғыны қағаздарды үйіп төгіп жинады", "ол арнайы келді", "бұл жоба бойынша жұмыс жүріп жатыр"]
RU = ["на рассмотрение парламента внесен проект закона о ратификации", "вы все приехали изо всех концов страны",
      "и эти деньги я повторю что сказала в своем выступлении", "это вопрос вообще очень не корректный"]
NB = CharNB().fit({"kk": KK * 3, "ru": RU * 3})


def test_russian_lines_are_dropped():
    assert label("вы все приехали и эти деньги не всех", NB)[0] == "ru"
    assert label("я еще работая в қоғамдық келісім мы совместно с верховным судом", NB)[0] == "ru"


def test_kazakh_lines_are_kept_even_without_kazakh_letters():
    for t in ["осыдан жиырма жыл", "ыыы рахмет", "неше жыл отыр"]:
        assert label(t, NB)[0] != "ru", t


def test_code_switched_kazakh_is_mixed_not_dropped():
    assert label("мастер класс өткіземіз отдельно", NB)[0] in ("mixed", "kk")
